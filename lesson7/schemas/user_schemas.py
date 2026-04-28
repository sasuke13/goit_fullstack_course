from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class UserRequestSchema(BaseModel):
    id: int | None = Field(None, description="The ID of the user")
    username: str = Field("username", min_length=3, max_length=10, description="The username of the user")
    password: str = Field("password", min_length=8, max_length=10, description="The password of the user")
    email: EmailStr
    created_at: datetime | None = Field(None, description="The creation date of the user")
    updated_at: datetime | None = Field(None, description="The last update date of the user")
