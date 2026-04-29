from datetime import UTC, datetime, timedelta
from typing import Literal, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jose import JWTError, jwt
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from config import settings
from db import User, get_db

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
http_bearer = HTTPBearer()
SCENARIO = settings.scenario


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
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


async def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    if expires_delta:
        return create_token(data, timedelta(seconds=expires_delta), "access")
    return create_token(
        data,
        timedelta(minutes=settings.access_token_expire_minutes),
        "access",
    )


async def create_refresh_token(data: dict, expires_delta: Optional[int] = None) -> str:
    if expires_delta:
        return create_token(data, timedelta(seconds=expires_delta), "refresh")
    return create_token(
        data,
        timedelta(minutes=settings.refresh_token_expire_minutes),
        "refresh",
    )


async def get_current_user_oauth(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
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


async def get_current_user_bearer(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_cookies(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = request.cookies.get("access_token")
    if token is None:
        raise credentials_exception

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
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


def verify_refresh_token_stateless(refresh_token: str) -> str | None:
    try:
        payload = jwt.decode(
            refresh_token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        username: str | None = payload.get("sub")
        token_type: str | None = payload.get("token_type")
        if username is None or token_type != "refresh":
            return None
        return username
    except JWTError:
        return None


def verify_refresh_token_db(refresh_token: str, db: Session) -> User | None:
    try:
        payload = jwt.decode(
            refresh_token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        username: str | None = payload.get("sub")
        token_type: str | None = payload.get("token_type")
        if username is None or token_type != "refresh":
            return None
        return (
            db.query(User)
            .filter(User.username == username, User.refresh_token == refresh_token)
            .first()
        )
    except JWTError:
        return None


# =========================================================
# HOT SWAP ZONE (auto-wired by scenario from config.py)
# =========================================================
if SCENARIO == "single_token_bearer":
    get_current_user = get_current_user_bearer
elif SCENARIO == "pair_tokens_cookies":
    get_current_user = get_current_user_cookies
else:
    get_current_user = get_current_user_oauth


def verify_refresh_token(refresh_token: str, db: Session | None = None):
    if SCENARIO == "pair_tokens_db":
        if db is None:
            return None
        return verify_refresh_token_db(refresh_token, db)
    return verify_refresh_token_stateless(refresh_token)
