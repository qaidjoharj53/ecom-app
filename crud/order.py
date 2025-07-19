from typing import List, Tuple
from schemas.order import OrderCreate, OrderListItem
from bson import ObjectId

def create_order(db, order: OrderCreate) -> str:
    order_dict = order.dict()
    # Insert order as is
    result = db.orders.insert_one(order_dict)
    return str(result.inserted_id)

def list_orders_with_details(db, user_id: str, limit: int, offset: int) -> Tuple[List[OrderListItem], int]:
    pipeline = [
        {"$match": {"userId": user_id}},
        {"$sort": {"_id": 1}},
        {"$skip": offset},
        {"$limit": limit},
        
        # Flatten items array
        {"$unwind": "$items"},

        # Convert string productId to ObjectId for proper lookup
        {
            "$addFields": {
                "items.productObjectId": {"$toObjectId": "$items.productId"}
            }
        },
        
        # Join with products collection to get product details
        {
            "$lookup": {
                "from": "products",                    # Target collection to join with
                "localField": "items.productObjectId", # Field from current document (order)
                "foreignField": "_id",                 # Field from products collection
                "as": "productDetails"                 # Name for the joined data array
            }
        },
        
        # Flatten productDetails array
        {"$unwind": "$productDetails"},
        
        # Group items back together by order ID
        {
            "$group": {
                "_id": "$_id",
                # Rebuild items array with enriched product details
                "items": {
                    "$push": {
                        "productDetails": {
                            "id": {"$toString": "$productDetails._id"},
                            "name": "$productDetails.name"
                        },
                        "qty": "$items.qty"
                    }
                },
                # Calculate total order price
                "total": {"$sum": {"$multiply": ["$items.qty", "$productDetails.price"]}}
            }
        },
        
        # Final output - select which fields to return
        {
            "$project": {
                "id": {"$toString": "$_id"},  # Convert ObjectId to string for API response
                "total": 1,                   # Include calculated total
                "items": 1,                   # Include enriched items array
                "_id": 0                      # Exclude original _id field
            }
        }
    ]
    cursor = db.orders.aggregate(pipeline)
    orders = []
    
    # Convert pipeline results to OrderListItem objects
    for doc in cursor:
        orders.append(OrderListItem(
            id=doc["id"], 
            total=doc["total"],
            items=doc["items"]
        ))

    # If pipeline fails
    if not orders:
        # Fallback: manual data fetching
        raw_orders = list(db["orders"].find({"userId": user_id}).skip(offset).limit(limit))
        
        # Process each order manually
        for order in raw_orders:
            enriched_items = []
            order_total = 0.0
            
            # Process each item in the order
            for item in order.get("items", []):
                # Check if productId exists in the item
                if "productId" in item:
                    product = db["products"].find_one({"_id": ObjectId(item["productId"])})
                    if product:
                        # Calculate cost for this item and add to grand total
                        item_total = item["qty"] * product["price"]
                        order_total += item_total
                        
                        # Create enriched item with product details
                        enriched_items.append({
                            "productDetails": {
                                "id": str(product["_id"]),
                                "name": product["name"]
                            },
                            "qty": item["qty"]
                        })
            
            # Only add order if it has valid items
            if enriched_items:
                orders.append(OrderListItem(
                    id=str(order["_id"]), 
                    total=order_total,
                    items=enriched_items
                ))

    return orders
