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

    @field_validator("amount")
    def check_amout(cls, amount):
        if amount <= 0:
            raise ValueError("Количество монет не может быть равно меньше или равно нулю.")
        return amount

class TransactionResponse(BaseModel):
    id: int
    from_user: Optional[str]
    to_user: Optional[str]
    amount: int
    description: Optional[str]
    created_at: datetime.datetime

    class Config:
        from_attributes = True