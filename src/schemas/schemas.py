from pydantic import BaseModel, field_validator
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str
    coin: int = 1000
    merch_list: List[str]

class UserResponce(BaseModel):
    id: int
    username: str
    password: str
    coin: int

class MerchCreate(BaseModel):
    merchname: str
    price: int

class MerchResponce(BaseModel):
    id: int
    merchname: str
    price: str