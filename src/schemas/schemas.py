from pydantic import BaseModel, field_validator
from typing import Optional
import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    coin: int = 1000

class UserResponce(BaseModel):
    id: int
    username: str
    coin: int

    class Config:
        from_attributes = True

class MerchCreate(BaseModel):
    merchname: str
    price: int

class MerchResponce(BaseModel):
    id: int
    merchname: str
    price: int

    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    receiver_username: str
    amount: int
    description: Optional[str] = None


class TransactionResponse(BaseModel): 
    to_user: str | None 
    amount: int
    description: str | None
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class IncomingTransactionResponce(BaseModel):
    from_user: str | None
    amount: int
    description: str | None
    created_at: datetime.datetime

    class Config:
        from_attributes = True