from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime
from .user_schema import UserResponse

class ReviewRequest(BaseModel):
    rating:int = Field(ge=1, le=5)
    comment:str

    @field_validator("comment")
    @classmethod
    def validate_comment(cls, value:str):
        value = value.strip()
        if not value:
            raise ValueError("comment cannot be empty")
        
        return value

class ReviewResponse(BaseModel):
    id:int
    user_id:int
    user:UserResponse
    product_id:int
    rating:int
    comment:str
    created_at:datetime | None
    updated_at:datetime | None

    model_config = ConfigDict(from_attributes=True)
