from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware


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

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis 

@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]

@app.post("/products")
def create(product: Product):
    return product.save()

def format(pk:str):
    product = Product.get(pk)
    return {
        'id': pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    } 

@app.get("/products/{pk}")
def get(pk: str):
    return Product.get(pk)

@app.delete("/products/{pk}")
def delete(pk: str):
    return Product.delete(pk)