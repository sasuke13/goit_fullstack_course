from datetime import UTC, datetime, timedelta
from typing import Literal, Optional

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from db import User, get_db

SECRET_KEY = "change_me_pair_tokens_cookies_secret"
ALGORITHM = "HS256"
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ACCESS_TOKEN_EXPIRE_MINUTES = 15
password_hash = PasswordHash.recommended()


class Hash:
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return password_hash.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return password_hash.hash(password)


def create_token(
    data: dict,
    expires_delta: timedelta,
    token_type: Literal["access", "refresh"],
) -> str:
    to_encode = data.copy()
    now = datetime.now(UTC)
    expire = now + expires_delta
    to_encode.update({"exp": expire, "iat": now, "token_type": token_type})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    if expires_delta:
        return create_token(data, timedelta(seconds=expires_delta), "access")
    return create_token(data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), "access")


async def create_refresh_token(data: dict, expires_delta: Optional[int] = None) -> str:
    if expires_delta:
        return create_token(data, timedelta(seconds=expires_delta), "refresh")
    return create_token(
        data,
        timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
        "refresh",
    )


def verify_refresh_token(refresh_token: str) -> str | None:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        token_type: str | None = payload.get("token_type")
        if username is None or token_type != "refresh":
            return None
        return username
    except JWTError:
        return None


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    token = request.cookies.get("access_token")
    if token is None:
        raise credentials_exception

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        token_type: str | None = payload.get("token_type")
        if username is None or token_type != "access":
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
