from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    Hash,
    create_access_token,
    create_refresh_token,
    get_current_user,
    verify_refresh_token,
)
from db import User, get_db

app = FastAPI(title="JWT Pair Tokens in Cookies Demo")
hash_handler = Hash()


class UserModel(BaseModel):
    username: str
    password: str


def set_token_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # For local demo only. Use True in production with HTTPS.
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # For local demo only. Use True in production with HTTPS.
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
    )


@app.post("/signup")
async def signup(body: UserModel, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == body.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists",
        )
    new_user = User(
        username=body.username,
        password=hash_handler.get_password_hash(body.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"new_user": new_user.username}


@app.post("/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username",
        )
    if not hash_handler.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )

    access_token = await create_access_token(data={"sub": user.username})
    refresh_token = await create_refresh_token(data={"sub": user.username})
    set_token_cookies(response, access_token, refresh_token)
    return {"message": "Login successful. Tokens are saved in HttpOnly cookies."}


@app.post("/refresh-token")
async def refresh_token(request: Request, response: Response):
    current_refresh_token = request.cookies.get("refresh_token")
    if current_refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token cookie is missing",
        )

    username = verify_refresh_token(current_refresh_token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    new_access_token = await create_access_token(data={"sub": username})
    new_refresh_token = await create_refresh_token(data={"sub": username})
    set_token_cookies(response, new_access_token, new_refresh_token)
    return {"message": "Tokens refreshed and updated in cookies."}


@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Logged out. Cookies are cleared."}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/secret")
async def secret(current_user: User = Depends(get_current_user)):
    return {"message": "secret route", "owner": current_user.username}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
