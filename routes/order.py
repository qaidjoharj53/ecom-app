from fastapi import APIRouter, Query, Path, status
from fastapi.responses import JSONResponse
from schemas.order import OrderCreate, OrderResponse, PaginatedOrdersResponse
from config.db import get_database
from crud.order import create_order, list_orders_with_details

# Initialize router with prefix and tags
router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_orders(order: OrderCreate):
    # Get database connection
    database = get_database()
    # Create new order in database
    order_id = create_order(database, order)
    # Return created order ID with 201 status
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": str(order_id)})

@router.get("/{user_id}", response_model=PaginatedOrdersResponse)
def get_orders(
    user_id: str = Path(..., description="User ID"),
    limit: int = Query(10, ge=1, description="Number of documents to return"),
    offset: int = Query(0, ge=0, description="Number of documents to skip for pagination")
):
    # Get database connection
    database = get_database()
    # Fetch orders with product details for specific user
    orders = list_orders_with_details(database, user_id, limit, offset)
    # Calculate next page offset
    next_offset = offset + limit
    # Calculate previous page offset
    previous_offset = offset - limit
    # Pagination metadata
    page = {
        "next": str(next_offset) if next_offset is not None else None,
        "limit": len(orders),
        "previous": int(previous_offset) if previous_offset is not None else None
    }
    # Return orders with pagination info
    return {"data": orders, "page": page}