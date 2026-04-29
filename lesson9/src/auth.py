from jose import jwt, JWTError
from pwdlib import PasswordHash
from datetime import timedelta, datetime, UTC
from typing import Optional

from fastapi import Depends, HTTPException, Response, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.config import settings
from src.db import User, get_db

password_hasher = PasswordHash.recommended()


class Hasher:
    def hash_password(self, password: str) -> str:
        return password_hasher.hash(password)
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        return password_hasher.verify(password, hashed_password)


def create_token(
    data: dict,
    expires_delta: timedelta,
    token_type: str = "access"
) -> str:
    to_encode = data.copy()
    now = datetime.now(UTC)
    expire = now + expires_delta
    to_encode.update({"exp": expire, "iat": now, "token_type": token_type})
    
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    expires_delta = expires_delta or settings.access_token_expire_minutes * 60

    return create_token(data, timedelta(seconds=expires_delta), "access")

def create_refresh_token(data: dict, expires_delta: Optional[int] = None) -> str:
    expires_delta = expires_delta or settings.refresh_token_expire_minutes * 60

    return create_token(data, timedelta(seconds=expires_delta), "refresh")


def set_token_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.refresh_token_expire_minutes * 60
    )

def verify_refresh_token(refresh_token: str, db: Session) -> User | None:
    try:
        payload = jwt.decode(
            refresh_token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        username: str | None = payload.get("sub")
        token_type: str | None = payload.get("token_type")
        
        if not username or not token_type or token_type != "refresh":
            return None

        return (
            db.query(User)
            .filter(User.username == username, User.refresh_token == refresh_token)
            .first()
        )
    except JWTError:
        return None

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    token = credentials.credentials
    
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        
        username: str | None = payload.get("sub")
        token_type: str | None = payload.get("token_type") 
        
        if not username or not token_type or token_type != "access":
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise credentials_exception
    
    return user


# def get_current_user(
#     request: Request,
#     db: Session = Depends(get_db)
# ) -> User:
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"}
#     )
    
#     token = request.cookies.get("access_token")
#     if not token:
#         raise credentials_exception
    
#     try:
#         payload = jwt.decode(
#             token,
#             settings.secret_key,
#             algorithms=[settings.algorithm]
#         )
        
#         username: str | None = payload.get("sub")
#         token_type: str | None = payload.get("token_type") 
        
#         if not username or not token_type or token_type != "access":
#             raise credentials_exception

#     except JWTError:
#         raise credentials_exception
    
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         raise credentials_exception
    
#     return user
