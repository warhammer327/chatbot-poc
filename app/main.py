from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from io import StringIO
import logging
import os

import weaviate
from weaviate.exceptions import WeaviateConnectionError
from weaviate.classes.config import Configure
from langchain_community.vectorstores import Weaviate

from app.database import get_db
from app.models import Product, Customer, PurchaseHistory
from app.schemas.product import ProductResponse
from app.schemas.customer import CustomerResponse
from app.schemas.purchase_history import PurchaseHistoryResponse


app = FastAPI(title="chatbot")


@app.get("/")
def status_check():
    return {"message": "app is on"}


@app.get("/products/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


@app.post("/products/")
async def create_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        decoded_file = pd.read_csv(StringIO(contents.decode("utf-8")))
        for index, row in decoded_file.iterrows():
            product = Product(
                product_name=row["product_name"],
                category=row["category"],
                price_per_unit=row["price_per_unit"],
                brand=row["brand"],
                product_description=row["product_description"],
            )
            db.add(product)

        db.commit()
        return {"status_code": 200, "message": "success"}

    except KeyError as e:
        logging.error(f"Missing column in CSV: {e}")
        raise HTTPException(status_code=400, detail=f"Missing column in CSV: {str(e)}")

    except ValueError as e:
        logging.error(f"Invalid data format: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid data format: {str(e)}")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return customer


@app.post("/customers/")
async def create_customer(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        decoded_file = pd.read_csv(StringIO(contents.decode("utf-8")))
        for index, row in decoded_file.iterrows():
            customer = Customer(
                first_name=row["first_name"],
                last_name=row["last_name"],
                gender=row["gender"],
                date_of_birth=row["date_of_birth"],
                email=row["email"],
                phone_number=row["phone_number"],
                signup_date=row["signup_date"],
                address=row["address"],
                city=row["city"],
                state=row["state"],
                zip_code=row["zip_code"],
            )
            db.add(customer)

        db.commit()

        return {"status_code": 200, "message": "success"}

    except KeyError as e:
        logging.error(f"Missing column in CSV: {e}")
        raise HTTPException(status_code=400, detail=f"Missing column in CSV: {str(e)}")

    except ValueError as e:
        logging.error(f"Invalid data format: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid data format: {str(e)}")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get(
    "/purchase_histories/{purchase_history_id}", response_model=PurchaseHistoryResponse
)
def read_purchase_history(purchase_history_id: int, db: Session = Depends(get_db)):
    purchase_history = (
        db.query(PurchaseHistory)
        .filter(PurchaseHistory.id == purchase_history_id)
        .first()
    )
    if purchase_history is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return purchase_history


@app.post("/purchase_histories/")
async def create_purchase_history(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    try:
        contents = await file.read()
        decoded_file = pd.read_csv(StringIO(contents.decode("utf-8")))
        for index, row in decoded_file.iterrows():
            purchase_history = PurchaseHistory(
                customer_id=row["customer_id"],
                product_id=row["product_id"],
                purchase_date=row["purchase_date"],
                quantity=row["quantity"],
                total_amount=row["total_amount"],
            )
            db.add(purchase_history)

        db.commit()

        return {"status_code": 200, "message": "success"}

    except KeyError as e:
        logging.error(f"Missing column in CSV: {e}")
        raise HTTPException(status_code=400, detail=f"Missing column in CSV: {str(e)}")

    except ValueError as e:
        logging.error(f"Invalid data format: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid data format: {str(e)}")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/check_weaviate")
def connect_to_weaviate():
    """
    Establish an async connection to the Weaviate client running in Docker
    and verify the connection
    """
    try:
        client = weaviate.connect_to_local(
            host="weaviate",  # Docker service name
            port=8087,
        )
        # Attempt to check connection
        try:
            return {
                "status": 200,
                "message": "Successfully connected to Weaviate",
                "is_ready": client.is_ready(),
                # "meta_data": client.get_meta(),
            }

        except Exception as e:
            logging.error(f"Weaviate connection or health check failed: {e}")
            raise HTTPException(
                status_code=500, detail=f"Weaviate health check failed: {str(e)}"
            )

    except WeaviateConnectionError as e:
        logging.error(f"Failed to connect to Weaviate: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Could not establish connection to Weaviate: {str(e)}",
        )

    except Exception as e:
        logging.error(f"Unexpected error connecting to Weaviate: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
