from pydantic import BaseModel
from datetime import datetime


class ProductBase(BaseModel):
    product_name: str
    category: str
    price_per_unit: float
    brand: str
    product_description: str


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
