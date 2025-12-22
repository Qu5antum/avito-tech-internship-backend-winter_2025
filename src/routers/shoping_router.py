from fastapi import APIRouter, status, Depends, HTTPException
from src.services.shoping_service import get_merch
from src.database.db import get_session, AsyncSession
from src.schemas.schemas import MerchCreate
from src.models.models import Personel
from src.security.security import get_current_user

router = APIRouter(
    prefix="/shop",
    tags=["shop"]
)

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_merchs(user: Personel = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await get_merch(session, user.id)

