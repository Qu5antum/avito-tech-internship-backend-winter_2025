from sqlalchemy import String, Integer, Column
from src.database.db import Base

class Personel(Base):
    __tablename__ = "personels"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    coin = Column(Integer)

class Merch(Base):
    __tablename__ = "merchs"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    merchname = Column(String)
    price = Column(Integer)

#Transaction class