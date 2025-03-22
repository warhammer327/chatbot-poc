from pydantic import BaseModel


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    pass

    class Config:
        from_attributes = True
