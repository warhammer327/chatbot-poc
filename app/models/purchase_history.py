from sqlalchemy import Column, Integer, Float, DateTime, func
from app.models.base import Base


class PurchaseHistory(Base):
    __tablename__ = "purchase_histories"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer)
    product_id = Column(Integer)
    purchase_date = Column(DateTime)
    quantity = Column(Integer)
    total_amount = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
