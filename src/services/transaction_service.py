from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import selectinload, aliased
from src.database.db import AsyncSession
from src.models.models import Transaction, Personel
from sqlalchemy import select
from src.schemas.schemas import TransactionResponse, IncomingTransactionResponce

# реализовать функцию для того чтобы пользователи могли отслеживать свои транзакции
async def get_transaction_history_by_user_id(
        session: AsyncSession,
        user_id: int, 
        receiver_username: str,
):
    if receiver_username is None:
        query = (
            select(Transaction)
            .where(Transaction.sender_id == user_id)
            .options(selectinload(Transaction.receiver))
            .order_by(Transaction.created_at.desc())
        )
    if receiver_username:
        Receiver = aliased(Personel)
        query = (
            select(Transaction)
            .join(Receiver, Transaction.receiver)
            .where(
                Transaction.sender_id == user_id,
                Receiver.username == receiver_username
            )
            .options(selectinload(Transaction.receiver))
            .order_by(Transaction.created_at.desc())
        )

    result = await session.execute(query)
    transactions = result.scalars().all()
    return [
        TransactionResponse(
            to_user=f"Перевод пользователю {t.receiver.username}" if t.receiver else None,
            amount=t.amount,
            description=t.description,
            created_at=t.created_at
        )
        for t in transactions
    ]
 

async def get_sending_history_by_user_id(
        session: AsyncSession,
        user_id: int,
        sender_name: str,
):
    if sender_name is None:
        query = (
            select(Transaction)
            .where(Transaction.receiver_id == user_id)
            .options(selectinload(Transaction.sender))
            .order_by(Transaction.created_at.desc())
        )
    if sender_name:
        Sender = aliased(Personel)

        query = (
            select(Transaction)
            .join(Sender, Transaction.sender)
            .where(
                Transaction.receiver_id == user_id, 
                Sender.username == sender_name
            )
            .options(selectinload(Transaction.sender))
            .order_by(Transaction.created_at.desc())
        )

    result = await session.execute(query)
    receives = result.scalars().all()

    return [
        IncomingTransactionResponce(
            from_user=f"Перевод от {t.sender.username}",
            amount=t.amount,
            description=t.description,
            created_at=t.created_at
        )
        for t in receives
    ]
