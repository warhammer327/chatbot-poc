from pydantic import BaseModel


class PurhcaseHistoryBase(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    total_amount: float


class PurchaseHistoryCreate(PurhcaseHistoryBase):
    pass


class PurchaseHistoryResponse(PurhcaseHistoryBase):
    pass

    class Config:
        from_attributes = True
