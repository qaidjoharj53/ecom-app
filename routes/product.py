from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from typing import Optional
from schemas.product import ProductCreate, ProductResponse, PaginatedProductsResponse
from config.db import get_database
from crud.product import create_product, list_products

# Initialize router with prefix and tags
router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_products(product: ProductCreate):
    # Get database connection
    database = get_database()
    # Create new product in database
    product_id = create_product(database, product)
    # Return created product ID with 201 status
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": str(product_id)})

@router.get("", response_model=PaginatedProductsResponse)
def get_products(
    name: Optional[str] = Query(None, description="Name filter, supports partial/regex search"),
    size: Optional[str] = Query(None, description="Filter products by size"),
    limit: int = Query(10, ge=1, description="Number of documents to return"),
    offset: int = Query(0, ge=0, description="Number of documents to skip for pagination")
):
    # Get database connection
    database = get_database()
    # Fetch products with optional filters and pagination
    products = list_products(database, name, size, limit, offset)
    # Calculate next page offset
    next_offset = offset + limit
    # Calculate previous page offset
    previous_offset = offset - limit
    # Pagination metadata
    page = {
        "next": str(next_offset) if next_offset is not None else None,
        "limit": len(products),
        "previous": int(previous_offset) if previous_offset is not None else None
    }
    # Return products with pagination info
    return {"data": products, "page": page}