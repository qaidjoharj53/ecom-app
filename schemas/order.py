from pydantic import BaseModel, Field
from typing import List

class OrderItem(BaseModel):
    productId: str
    qty: int = Field(gt=0)

class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]

class ProductDetails(BaseModel):
    id: str
    name: str

class OrderItemDetails(BaseModel):
    productDetails: ProductDetails
    qty: int

class OrderResponse(BaseModel):
    id: str

class OrderListItem(BaseModel):
    id: str
    items: List[OrderItemDetails]

class OrdersResponse(BaseModel):
    data: List[OrderListItem]