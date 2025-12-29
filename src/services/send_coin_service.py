from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import selectinload
from src.database.db import AsyncSession
from src.models.models import Transaction, Personel
from sqlalchemy import select
from src.schemas.schemas import TransactionCreate


async def send_coins(
        session: AsyncSession,
        sender_id: int,
        receiver_username: str,
        amount: int,
        description: str
):
    sender = await session.get(Personel, sender_id)

    query = select(Personel).where(Personel.username == receiver_username)
    result = await session.execute(query)
    receiver = result.scalar_one_or_none()

    if amount < 10:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Минимальное сумма для отправки не может быть меньше 10 монет.")
     
    if not receiver:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Пользователь под этим именем не найден.")
    
    if sender.id == receiver.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Нельзя отправить самому себе монеты.")

    if sender.coin < amount:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Недостаточно средств для отправки.")
    
    
    sender.coin -= amount
    receiver.coin += amount

    sending = Transaction(
        sender = sender,
        receiver = receiver,
        amount = amount,
        description = description
    )

    session.add(sending)
    await session.commit()
    await session.refresh(sending)

    return sending




    
    
