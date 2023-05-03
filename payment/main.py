from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import requests
import time
from fastapi.background import BackgroundTasks


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

redis = get_redis_connection(
    host="redis-14179.c258.us-east-1-4.ec2.cloud.redislabs.com",
    port=14179,
    password="hqCNKNsQT9InaSk1OMh4iWRmBHk5Ufom",
    decode_responses=True,
)

class Order(HashModel):
    product_id: str
    price: float
    fee : float
    total: float
    quantity: int
    status: str

    class Meta:
        database = redis

@app.get("/orders/{pk}")
def get(pk: str):
    return Order.get(pk)

@app.post("/orders")
async def create(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()

    req = requests.get(f"http://localhost:8000/products/%s" %body['id'])
    product = req.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=product['price'] * 0.2,
        total=product['price'] * 1.2,
        quantity=body['quantity'],
        status='pending'
    )
    order.save()

    background_tasks.add_task(order_completed, order)
    return order


def order_completed(order: Order):
    time.sleep(4)
    order.status = 'completed'
    order.save()

