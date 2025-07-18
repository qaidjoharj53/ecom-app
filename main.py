from fastapi import FastAPI
from routes.product import router as products_router
from routes.order import router as orders_router
from config.db import get_database

app = FastAPI()

# Initialize database connection
db_instance = get_database()

# Include routers
app.include_router(products_router)
app.include_router(orders_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Ecommerce API"}
