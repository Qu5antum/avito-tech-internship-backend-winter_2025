from fastapi import APIRouter, status, Depends, HTTPException
from src.services.send_coin_service import send_coins
from src.database.db import get_session, AsyncSession
from src.schemas.schemas import TransactionCreate
from src.models.models import Personel, Transaction
from src.security.security import get_current_user

router = APIRouter(
    prefix="/sends",
    tags=["sends"]
)

@router.post("", status_code=status.HTTP_200_OK)
async def send_coins_to_user(
    amount: int,
    receiver: str,
    sender: Personel = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await send_coins(session=session, sender_id=sender.id, receiver_username=receiver, amount=amount)