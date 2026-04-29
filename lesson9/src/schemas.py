from pydantic import BaseModel


class UserResponseModel(BaseModel):
    username: str


class UserModel(UserResponseModel):
    password: str


class MessageModel(BaseModel):
    message: str


class AccessTokenModel(BaseModel):
    access_token: str

    token_type: str = "Bearer"


class TokenModel(AccessTokenModel):
    refresh_token: str
