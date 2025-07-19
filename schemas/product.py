from pydantic import BaseModel, Field
from typing import List
from .common import BasePaginatedResponse

class SizeQuantity(BaseModel):
    size: str
    quantity: int = Field(ge=0)

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[SizeQuantity]

class ProductResponse(BaseModel):
    id: str

class ProductListItem(BaseModel):
    id: str
    name: str
    price: float

class PaginatedProductsResponse(BasePaginatedResponse):
    data: List[ProductListItem]