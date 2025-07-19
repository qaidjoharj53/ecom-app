from typing import List
from schemas.order import OrderCreate, OrderListItem

def create_order(db, order: OrderCreate) -> str:
    order_dict = order.dict()
    result = db.orders.insert_one(order_dict)
    return str(result.inserted_id)

def list_orders_with_details(db, user_id: str) -> List[OrderListItem]:
    pipeline = [
        {"$match": {"userId": user_id}},
        {"$sort": {"_id": 1}},
        {"$unwind": "$items"},
        {
            "$lookup": {
                "from": "products",
                "localField": "items.productId",
                "foreignField": "_id",
                "as": "productDetails"
            }
        },
        {"$unwind": "$productDetails"},
        {
            "$group": {
                "_id": "$_id",
                "items": {
                    "$push": {
                        "productDetails": {
                            "id": {"$toString": "$productDetails._id"},
                            "name": "$productDetails.name"
                        },
                        "qty": "$items.qty"
                    }
                }
            }
        },
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "items": 1,
                "_id": 0
            }
        }
    ]
    cursor = db.orders.aggregate(pipeline)
    orders = []
    for doc in cursor:
        orders.append(OrderListItem(id=doc["id"], items=doc["items"]))
    return orders