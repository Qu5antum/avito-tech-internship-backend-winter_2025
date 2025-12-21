from fastapi import HTTPException, status
from src.database.db import AsyncSession
from src.models.models import Personel
from src.schemas.schemas import UserCreate
from sqlalchemy import select

async def create_new_user(session: AsyncSession, user: UserCreate):
    query = select(Personel).where(Personel.username == user.username)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует."
        )
    
    new_user = Personel(
        username = user.username,
        password = user.password,
        coin = user.coin
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user

    
