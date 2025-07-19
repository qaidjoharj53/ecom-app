from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from typing import Optional
from schemas.product import ProductCreate, ProductResponse, ProductsResponse
from config.db import get_database
from crud.product import create_product, list_products

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_products(product: ProductCreate):
    database = get_database()
    product_id = create_product(database, product)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": str(product_id)})

@router.get("", response_model=ProductsResponse)
def get_products(
    name: Optional[str] = Query(None, description="Name filter, supports partial/regex search"),
    size: Optional[str] = Query(None, description="Filter products by size")
):
    database = get_database()
    products = list_products(database, name, size)
    return {"data": products}