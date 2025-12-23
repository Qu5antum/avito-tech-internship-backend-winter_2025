from fastapi import APIRouter, status, Depends, HTTPException
from src.services.shoping_service import get_all_merch, buy_merch, get_purchase_by_user_id
from src.database.db import get_session, AsyncSession
from src.schemas.schemas import MerchCreate
from src.models.models import Personel
from src.security.security import get_current_user

router = APIRouter(
    prefix="/shop",
    tags=["shop"]
)

@router.get("/show_merch", status_code=status.HTTP_200_OK)
async def get_all_merchs(user: Personel = Depends(get_current_user),
                        session: AsyncSession = Depends(get_session)
    ):
    return await get_all_merch(session, user.id)

@router.post("/{user_id}", status_code=status.HTTP_200_OK)
async def buy_merch_in_shop(merch_name: str,
                            user: Personel = Depends(get_current_user),
                            session: AsyncSession = Depends(get_session)
    ):
    return await buy_merch(session=session, user_id=user.id, merch_name=merch_name)

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_all_purchase_from_user(user: Personel = Depends(get_current_user),
                                    session: AsyncSession = Depends(get_session)
    ):
    return await get_purchase_by_user_id(session=session, user_id=user.id)

