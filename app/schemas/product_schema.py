from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas import CategoryResponse
from enum import Enum

class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    stock_quantity: int
    category_id: int

class ProductUpdate(BaseModel):
    name: str
    description: str
    price: int
    stock_quantity: int
    category_id: int
    is_active:bool

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    stock_quantity: int
    category_id: int
    is_active: bool
    image: str | None = None

    average_rating: float | None = None
    review_count: int = 0

    created_at: datetime | None
    updated_at: datetime | None
    category: CategoryResponse | None

    model_config = ConfigDict(from_attributes=True)

class ProductSortFields(str, Enum):
    name = "name"
    price = "price"
    stock_quantity = "stock_quantity"
    created_at = "created_at"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

class ProductListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[ProductResponse]