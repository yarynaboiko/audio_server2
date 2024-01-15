from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

products = {}

class Product(BaseModel):
    name: str = Field(title = "Назва товару", min_length=3, max_length=100)
    description: str = Field(title = "Опис товару", min_length=5, max_length=1000)


@app.get("/")
def index():
    return "Hello FastAPI!"

@app.post("/products/")
def add_product(product: Product):
    if product.name not in products:
        products[product.name] = product.description
        return {"mesaage": "Товар додано"}
    else:
        return {"msg": "Такий товар вже існує"}

@app.get("/products/all")
def get_all_products():
    return products

@app.put("/products/{product_name}")
def update_products(product_name: str, description: str):
    if product_name in products:
        products[product_name] = description
        return {"mesaage": "Товар оновлено"}
    else:
        return {"msg": "Такий товар не існує"}
    
@app.delete("/products/{product_name}")
def delete_products(product_name: str):
    if product_name in products:
        del products[product_name]
        return{"msg":"Товар видалено"}
    else:
        return {"msg": "Такий товар не існує"}
        
@app.get("/products/{product_name}")
def get_products(product_name: Annotated[str, Path(title="Назва продукту", description = "Введіть опис продукту", min_length=5, max_length=1000)]):
    if product_name in products:
        return products[product_name]
    else:
        return {"msg": "Такий товар не існує"}