from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.models.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    brand = Column(String, nullable=False)
    product_description = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
