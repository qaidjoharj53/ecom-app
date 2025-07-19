from fastapi import APIRouter, Path, status
from fastapi.responses import JSONResponse
from schemas.order import OrderCreate, OrderResponse, OrdersResponse
from config.db import get_database
from crud.order import create_order, list_orders_with_details

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_orders(order: OrderCreate):
    database = get_database()
    order_id = create_order(database, order)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": str(order_id)})

@router.get("/{user_id}", response_model=OrdersResponse)
def get_orders(user_id: str = Path(..., description="User ID")):
    database = get_database()
    orders = list_orders_with_details(database, user_id)
    return {"data": orders}