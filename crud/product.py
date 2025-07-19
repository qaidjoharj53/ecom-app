from typing import Optional, List, Tuple
from schemas.product import ProductCreate, ProductListItem
from pymongo import ASCENDING
import re

def create_product(db, product: ProductCreate) -> str:
    product_dict = product.dict()
    # Convert sizes list of dicts as is
    result = db.products.insert_one(product_dict)
    return str(result.inserted_id)

def list_products(db, name: Optional[str], size: Optional[str], limit: int, offset: int) -> Tuple[List[ProductListItem], int]:
    query = {}
    if name:
        # Use case-insensitive regex for partial match
        query["name"] = {"$regex": re.escape(name), "$options": "i"}
    if size:
        # Filter products that have sizes with size field matching the size param
        query["sizes.size"] = size

    cursor = db.products.find(query).sort("_id", ASCENDING).skip(offset).limit(limit)
    products = []
    for doc in cursor:
        products.append(ProductListItem(id=str(doc["_id"]), name=doc["name"], price=doc["price"]))
    return products