from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Product
from app.schemas.product import ProductCreate, ProductResponse

app = FastAPI(title="chatbot")


@app.get("/")
def status_check():
    return {"message": "app is on"}


@app.get("/products/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    cur_product = Product(**product.dict())
    print("--------------------")
    print(cur_product)
    print("--------------------")
    db.add(cur_product)
    db.commit()
    db.refresh(cur_product)
    return cur_product


@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
