from pydantic import BaseModel, Field
from typing import List

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

class ProductsResponse(BaseModel):
    data: List[ProductListItem]