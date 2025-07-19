from typing import Optional, List
from schemas.product import ProductCreate, ProductListItem
from bson import ObjectId
from pymongo import ASCENDING
import re

def create_product(db, product: ProductCreate) -> str:
    product_dict = product.dict()
    result = db.products.insert_one(product_dict)
    return str(result.inserted_id)

def list_products(db, name: Optional[str] = None, size: Optional[str] = None) -> List[ProductListItem]:
    query = {}
    if name:
        query["name"] = {"$regex": re.escape(name), "$options": "i"}
    if size:
        query["sizes.size"] = size

    cursor = db.products.find(query).sort("_id", ASCENDING)
    products = []
    for doc in cursor:
        products.append(ProductListItem(id=str(doc["_id"]), name=doc["name"], price=doc["price"]))
    return products