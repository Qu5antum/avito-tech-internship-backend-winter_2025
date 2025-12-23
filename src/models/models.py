from sqlalchemy import String, Integer, Column, ForeignKey, Table, DateTime, func
from sqlalchemy.orm import relationship
from src.database.db import Base

#many to many from Merch to Personel
class PersonelMerch(Base):
    __tablename__ = "personels_merch"

    id = Column(Integer, primary_key=True, unique=True, index=True)

    personel_id = Column(Integer, ForeignKey("personels.id"), index=True)
    merch_id = Column(Integer, ForeignKey("merchs.id"), index=True)

    quantity = Column(Integer, default=1, nullable=False)
    purchased_at = Column(DateTime(timezone=True), server_default=func.now())

    personel = relationship("Personel", back_populates="merch_list")
    merch = relationship("Merch", back_populates="merch_list")

class Personel(Base):
    __tablename__ = "personels"

    id = Column(Integer, primary_key=True, unique=True, index=True)

    username = Column(String, unique=True)
    password = Column(String)
    coin = Column(Integer, nullable=False)
    merch_list = relationship("PersonelMerch", back_populates="personel", cascade="all, delete-orphan")

    sent_transactions = relationship("Transaction", foreign_keys="Transaction.sender_id", back_populates="sender")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.receiver_id", back_populates="receiver")
    

class Merch(Base):
    __tablename__ = "merchs"

    id = Column(Integer, primary_key=True, unique=True, index=True)

    merchname = Column(String, unique=True)
    price = Column(Integer)
    merch_list = relationship("PersonelMerch", back_populates="merch")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, unique=True, index=True)

    sender_id = Column(Integer, ForeignKey("personels.id"), nullable=True)
    receiver_id = Column(Integer, ForeignKey("personels.id"), nullable=True)

    amount = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sender = relationship("Personel", foreign_keys=[sender_id], back_populates="sent_transactions")
    receiver = relationship("Personel", foreign_keys=[receiver_id], back_populates="received_transactions")

