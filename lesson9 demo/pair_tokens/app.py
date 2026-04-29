from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth import (
    Hash,
    create_access_token,
    create_refresh_token,
    get_current_user,
    verify_refresh_token,
)
from db import User, get_db

app = FastAPI(title="JWT Pair Tokens Demo")
hash_handler = Hash()


class UserModel(BaseModel):
    username: str
    password: str


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


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


@app.post("/login", response_model=TokenModel)
async def login(
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
    user.refresh_token = refresh_token
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@app.post("/refresh-token", response_model=TokenModel)
async def new_token(request: TokenRefreshRequest, db: Session = Depends(get_db)):
    user = verify_refresh_token(request.refresh_token, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    new_access_token = await create_access_token(data={"sub": user.username})
    return {
        "access_token": new_access_token,
        "refresh_token": request.refresh_token,
        "token_type": "bearer",
    }


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/secret")
async def secret(current_user: User = Depends(get_current_user)):
    return {"message": "secret route", "owner": current_user.username}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
