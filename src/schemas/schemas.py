from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    coin: int

class UserResponce(BaseModel):
    id: int
    username: str
    password: str
    coin: int