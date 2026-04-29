from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    password: str


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class AccessTokenModel(BaseModel):
    access_token: str
    token_type: str


class MessageModel(BaseModel):
    message: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str
