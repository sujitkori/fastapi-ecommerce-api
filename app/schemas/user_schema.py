from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from app.enums import UserRole

class UserCreate(BaseModel):
    name: str
    email : EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

   

class UserProfileResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(from_attributes=True)