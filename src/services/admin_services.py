from fastapi import HTTPException, status, Depends
from src.database.db import AsyncSession
from src.models.models import Merch, Personel
from src.schemas.schemas import MerchCreate
from sqlalchemy import select
from src.security.security import get_current_user

async def add_merch(
        session: AsyncSession,
        merch: str,
    ):
    query = select(Merch).where(Merch.merchname == merch.merchname)
    result = await session.execute(query)
    existing_merch = result.scalar_one_or_none()

    if existing_merch:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Такой товар уже имеется в каталоге.")
    
    new_merch = Merch(
        merchname = merch.merchname,
        price = merch.price
    )

    session.add(new_merch)
    await session.commit()
    await session.refresh(new_merch)

    return new_merch


