from fastapi import FastAPI
from redis_om import get_redis_connection

app = FastAPI()
redis = get_redis_connection(
    host="redis-14179.c258.us-east-1-4.ec2.cloud.redislabs.com",
    port=14179,
    password="hqCNKNsQT9InaSk1OMh4iWRmBHk5Ufom",
    decode_responses=True,
)

class Product(Hashmodel):
    name: str
    price: float
    quantity: int 

@app.get("/")
async def root():
    return {"message": "Hello World"}
