from fastapi import HTTPException, status, Depends
from src.database.db import AsyncSession
from src.models.models import Merch, Personel
from src.schemas.schemas import MerchCreate
from sqlalchemy import select
from src.security.security import get_current_user

async def buy_merch(session: AsyncSession, user_id: int, merch_name: str):
    # проверка на существование мерча
    merch_query = select(Merch).where(Merch.merchname == merch_name)
    merch_result = await session.execute(merch_query)
    existing_merch = merch_result.scalar_one_or_none()

    if existing_merch is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Этот продукт не найден.")
    
    # вывод цены для мерча
    price_query = select(Merch.price).where(Merch.merchname == merch_name)
    price_result = await session.execute(price_query)
    merch_price = price_result.scalar_one()

    # вывод баланса пользователя
    coin_query = select(Personel.coin).where(Personel.id == user_id)
    coin_result = await session.execute(coin_query)
    coin_existing = coin_result.scalar_one_or_none()

    if coin_existing < merch_price:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Недостаточно баланса для покупки.")
    
    




async def get_merch(session: AsyncSession, user_id: int):
    user = await session.get(Personel, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Пользоавтель не найден.")
    
    query = select(Merch.merchname, Merch.price)
    result = await session.execute(query)
    return result.mappings().all()