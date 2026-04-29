from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import (
    Hash,
    create_access_token,
    create_refresh_token,
    get_current_user,
    verify_refresh_token,
)
from config import settings
from db import User, get_db
from schemas import (
    AccessTokenModel,
    MessageModel,
    TokenModel,
    TokenRefreshRequest,
    UserModel,
)

app = FastAPI(title="JWT Hot Swap Bundle Demo")
hash_handler = Hash()
SCENARIO = settings.scenario
IS_SINGLE = SCENARIO in {"single_token", "single_token_bearer"}
IS_COOKIES = SCENARIO == "pair_tokens_cookies"
IS_DB_REFRESH = SCENARIO == "pair_tokens_db"

# =========================================================
# HOT SWAP ZONE (auto by config.ACTIVE_SCENARIO)
# =========================================================
LOGIN_RESPONSE_MODEL = MessageModel if IS_COOKIES else AccessTokenModel if IS_SINGLE else TokenModel
REFRESH_RESPONSE_MODEL = MessageModel if IS_COOKIES else AccessTokenModel if IS_SINGLE else TokenModel


def set_token_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Local demo only.
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # Local demo only.
        samesite="lax",
        max_age=settings.refresh_token_expire_minutes * 60,
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


@app.post("/login", response_model=LOGIN_RESPONSE_MODEL)
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
    if IS_SINGLE:
        return {"access_token": access_token, "token_type": "bearer"}

    refresh_token = await create_refresh_token(data={"sub": user.username})

    if IS_DB_REFRESH:
        user.refresh_token = refresh_token
        db.commit()

    if IS_COOKIES:
        set_token_cookies(response, access_token, refresh_token)
        return {"message": "Login successful. Tokens are saved in HttpOnly cookies."}

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@app.post("/refresh-token", response_model=REFRESH_RESPONSE_MODEL)
async def new_token(
    raw_request: Request,
    response: Response,
    db: Session = Depends(get_db),
    request: TokenRefreshRequest | None = None,
):
    if IS_SINGLE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh route is disabled for single token mode",
        )

    if IS_COOKIES:
        current_refresh_token = raw_request.cookies.get("refresh_token")
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

    if IS_DB_REFRESH:
        if request is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token is required in request body",
            )
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

    if request is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token is required in request body",
        )
    username = verify_refresh_token(request.refresh_token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    new_access_token = await create_access_token(data={"sub": username})
    return {
        "access_token": new_access_token,
        "refresh_token": request.refresh_token,
        "token_type": "bearer",
    }


@app.post("/logout", response_model=MessageModel)
async def logout(response: Response):
    if not IS_COOKIES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Logout route is enabled only for cookies mode",
        )
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
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
