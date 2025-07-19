# Ecommerce Backend API with FastAPI and MongoDB

## Project Overview

This project is a sample backend application for an ecommerce platform similar to Flipkart/Amazon. It is built using FastAPI (Python) and MongoDB (via MongoDB Atlas). The application provides RESTful APIs to create and list products, create orders, and retrieve orders for users with pagination and filtering support.

## Tech Stack

-   Python 3.12.3
-   FastAPI
-   PyMongo (for MongoDB driver)
-   Pydantic (for data validation)
-   MongoDB Atlas (Cloud-hosted MongoDB)
-   Uvicorn (ASGI server)
-   Gunicorn (WSGI server for production)
-   Docker (for containerization)

## Project Structure

```
.
├── main.py                 # FastAPI app entry point
├── config/
│   └── db.py               # MongoDB connection setup using PyMongo
├── crud/
│   ├── __init__.py
│   ├── product.py          # CRUD operations related to products
│   └── order.py            # CRUD operations related to orders
├── routes/
│   ├── __init__.py
│   ├── product.py          # API route handlers for product endpoints
│   └── order.py            # API route handlers for order endpoints
├── schemas/
│   ├── __init__.py
│   ├── common.py           # Common Pydantic models (e.g., pagination info)
│   ├── product.py          # Pydantic models for product request/response validation
│   └── order.py            # Pydantic models for order request/response validation
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker container setup
├── .dockerignore
├── .gitignore
└── README.md               # This documentation file
```

## Setup and Running Locally

1. **Clone the repository**

2. **Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure MongoDB connection**

Update the MongoDB connection URI in `config/db.py` to point to your MongoDB Atlas cluster or local MongoDB instance.

5. **Run the FastAPI application**

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## Deployment

The application is deployed on Render with MongoDB Atlas as the database backend. Ensure environment variables or config files are set appropriately for production deployment.

### 🔗 Deployed URL: https://ecom-app-09v1.onrender.com

---

## API Documentation

The API exposes the following endpoints:

### 1. Create Product

-   **Endpoint:** `POST /products`
-   **Request Body:**

```json
{
	"name": "string",
	"price": 100.0,
	"sizes": [
		{
			"size": "string",
			"quantity": 0
		}
	]
}
```

-   **Response Body:**

```json
{
	"id": "1234567890"
}
```

-   **Status Code:** 201 Created

### 2. List Products

-   **Endpoint:** `GET /products`
-   **Query Parameters (optional):**

    -   `name` (string): Partial or regex search on product name
    -   `size` (string): Filter products by size (e.g., "large")
    -   `limit` (int): Number of products to return (default 10)
    -   `offset` (int): Number of products to skip for pagination (default 0)

-   **Response Body:**

```json
{
	"data": [
		{
			"id": "12345",
			"name": "Sample",
			"price": 100.0
		},
		{
			"id": "12346",
			"name": "Sample 2",
			"price": 10.0
		}
	],
	"page": {
		"next": "10",
		"limit": 2,
		"previous": "0"
	}
}
```

-   **Status Code:** 200 OK

### 3. Create Order

-   **Endpoint:** `POST /orders`
-   **Request Body:**

```json
{
	"userId": "user_1", // Hardcoded
	"items": [
		{
			"productId": "123456789",
			"qty": 3
		},
		{
			"productId": "123456790",
			"qty": 3
		}
	]
}
```

-   **Response Body:**

```json
{
	"id": "1234567890"
}
```

-   **Status Code:** 201 Created

### 4. Get List of Orders for a User

-   **Endpoint:** `GET /orders/{user_id}`
-   **Path Parameter:**
    -   `user_id` (string): User ID to fetch orders for
-   **Query Parameters (optional):**

    -   `limit` (int): Number of orders to return (default 10)
    -   `offset` (int): Number of orders to skip for pagination (default 0)

-   **Response Body:**

```json
{
	"data": [
		{
			"id": "12345",
			"items": [
				{
					"productDetails": {
						"id": "123456",
						"name": "Sample Product"
					},
					"qty": 3
				}
			]
            "total": 300.0
		}
	],
	"page": {
		"next": "10",
		"limit": 1,
		"previous": -10
	}
}
```

-   **Status Code:** 200 OK

## Notes

-   Pagination is implemented using `limit` and `offset` query parameters.
-   Product filtering supports partial name matching and size filtering.
-   Order listing performs a MongoDB aggregation to join product details with order items.

## Contact

For any questions or issues, please contact the project maintainer - [Qaidjohar Jukker](https://qaidjoharj.me/).
