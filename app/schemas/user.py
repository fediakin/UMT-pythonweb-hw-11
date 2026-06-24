from pydantic import BaseModel, EmailStr

class UserModel(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    avatar: str | None
    confirmed: bool

    model_config = {"from_attributes": True}

class TokenModel(BaseModel):
    access_token: str
    token_type: str = "bearer"