from pydantic import BaseModel, Field
from typing import List
from .common import BasePaginatedResponse

class OrderItem(BaseModel):
    productId: str
    qty: int = Field(gt=0)

class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]

class OrderResponse(BaseModel):
    id: str

class ProductDetails(BaseModel):
    id: str
    name: str

class OrderItemDetails(BaseModel):
    productDetails: ProductDetails
    qty: int

class OrderListItem(BaseModel):
    id: str
    total: float = 0.0
    items: List[OrderItemDetails]

class PaginatedOrdersResponse(BasePaginatedResponse):
    data: List[OrderListItem]