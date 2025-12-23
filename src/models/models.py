from sqlalchemy import String, Integer, Column, ForeignKey, Table, DateTime, func
from sqlalchemy.orm import relationship
from src.database.db import Base

#many to many from Merch to Personel
class PersonelMerch(Base):
    __tablename__ = "personels_merch"

    id = Column(Integer, primary_key=True)
    personel_id = Column(Integer, ForeignKey("personels.id"), index=True)
    merch_id = Column(Integer, ForeignKey("merchs.id"), index=True)

    quantity = Column(Integer, default=1)
    purchased_at = Column(DateTime(timezone=True), server_default=func.now())

    personel = relationship("Personel", back_populates="merch_list")
    merch = relationship("Merch", back_populates="merch_list")

class Personel(Base):
    __tablename__ = "personels"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    coin = Column(Integer)
    merch_list = relationship("PersonelMerch", back_populates="personel", cascade="all, delete-orphan")


class Merch(Base):
    __tablename__ = "merchs"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    merchname = Column(String, unique=True)
    price = Column(Integer)
    merch_list = relationship("PersonelMerch", back_populates="merch")


#Transaction class