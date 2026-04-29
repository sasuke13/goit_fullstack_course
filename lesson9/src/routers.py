from fastapi import APIRouter, Request, Depends, HTTPException, Form, Response
from sqlalchemy.orm import Session

from src.schemas import UserModel, MessageModel, TokenModel, UserResponseModel, AccessTokenModel
from src.db import get_db, User

from src.auth import Hasher, create_access_token, create_refresh_token, get_current_user, verify_refresh_token, set_token_cookies
from src.config import settings


hasher = Hasher()
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=MessageModel)
async def register(user: UserModel, request: Request, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username, 
        password=hasher.hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


@router.post("/login", response_model=TokenModel)
async def login(user: UserModel, request: Request, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if not existing_user or not hasher.verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    refresh_token = create_refresh_token(data={"sub": existing_user.username})
    existing_user.refresh_token = refresh_token
    
    db.commit()
    db.refresh(existing_user)

    return {
        "access_token": create_access_token(data={"sub": existing_user.username}),
        "refresh_token": refresh_token
    }


# @router.post("/login", response_model=MessageModel)
# async def login(user: UserModel, response: Response, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter(User.username == user.username).first()
#     if not existing_user or not hasher.verify_password(user.password, existing_user.password):
#         raise HTTPException(status_code=401, detail="Invalid username or password")

#     set_token_cookies(
#         response,
#         create_access_token(data={"sub": existing_user.username}),
#         create_refresh_token(data={"sub": existing_user.username})
#     )

#     return {"message": "User logged in successfully"}


@router.post("/refresh", response_model=AccessTokenModel)
async def refresh(refresh_token: str = Form(...), db: Session = Depends(get_db)):
    user = verify_refresh_token(refresh_token, db)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    new_access_token = create_access_token(data={"sub": user.username})

    return {"access_token": new_access_token}


# @router.post("/refresh", response_model=MessageModel)
# async def refresh(request: Request, response: Response):
#     username = verify_refresh_token(request.cookies.get("refresh_token"))
    
#     if not username:
#         raise HTTPException(status_code=401, detail="Invalid refresh token")
    
#     new_access_token = create_access_token(data={"sub": username})

#     response.set_cookie(
#         key="access_token",
#         value=new_access_token,
#         httponly=True,
#         secure=False,
#         samesite="lax",
#         max_age=settings.access_token_expire_minutes * 60
#     )

#     return {"message": "Token refreshed successfully"}

# @router.post("/logout")
# async def logout(response: Response):
#     response.delete_cookie("access_token")
#     response.delete_cookie("refresh_token")

#     return {"message": "User logged out successfully"}


@router.get("/me", response_model=UserResponseModel)
async def me(request: Request, user: User = Depends(get_current_user)):
    return {"username": user.username}
