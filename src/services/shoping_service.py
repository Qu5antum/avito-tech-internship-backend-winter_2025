from fastapi import HTTPException, status, Depends
from src.database.db import AsyncSession
from src.models.models import Merch, Personel, PersonelMerch
from src.schemas.schemas import MerchCreate
from sqlalchemy import select
from src.security.security import get_current_user
from sqlalchemy.orm import selectinload

async def buy_merch(session: AsyncSession, user_id: int, merch_name: str):
    user_query = (
        select(Personel)
        .where(Personel.id == user_id)
        .options(selectinload(Personel.merch_list).selectinload(PersonelMerch.merch))
    )
    user_result = await session.execute(user_query)
    user = user_result.scalar_one_or_none()

    # проверка на существование мерча
    merch_query = select(Merch).where(Merch.merchname == merch_name)
    merch_result = await session.execute(merch_query)
    merch = merch_result.scalar_one_or_none()

    if merch is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Этот продукт не найден.")

    if user.coin < merch.price:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Недостаточно баланса для покупки.")
    
    purchase = next((i for i in user.merch_list if i.merch_id == merch.id), None)

    if purchase:
        purchase.quantity += 1
    else:
        session.add(PersonelMerch(personel=user, merch=merch, quantity=1))
    
    user.coin -= merch.price

    await session.commit()

    return {"detail": "Покупка успешна"}


async def get_purchase_by_user_id(session: AsyncSession, user_id: int):
    query = (
        select(Personel)
        .where(Personel.id == user_id)
        .options(selectinload(Personel.merch_list).selectinload(PersonelMerch.merch))
    )
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    return user.merch_list

    
async def get_all_merch(session: AsyncSession, user_id: int):
    query = select(Merch.merchname, Merch.price)
    result = await session.execute(query)
    return result.mappings().all()