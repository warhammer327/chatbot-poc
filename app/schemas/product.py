from pydantic import BaseModel


class ProductBase(BaseModel):
    product_name: str
    category: str
    price_per_unit: float
    brand: str
    product_description: str


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    pass

    class Config:
        from_attributes = True
