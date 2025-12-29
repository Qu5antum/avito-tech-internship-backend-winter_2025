from fastapi import APIRouter, status, Depends, HTTPException
from src.services.send_coin_service import send_coins
from src.database.db import get_session, AsyncSession
from src.schemas.schemas import TransactionCreate
from src.models.models import Personel, Transaction
from src.security.security import get_current_user
from src.services.transaction_service import get_transaction_history_by_user_id, get_sending_history_by_user_id

router = APIRouter(
    prefix="/transaction",
    tags=["transactions"]
)

@router.get("/sendings", status_code=status.HTTP_200_OK)
async def get_transaction_history(
    recevier_username: str | None = None,
    user: Personel = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await get_transaction_history_by_user_id(
        session=session,
        user_id=user.id,
        receiver_username=recevier_username,
    )

@router.get("/receives", status_code=status.HTTP_200_OK)
async def get_sending_history(
    sender_username: str | None = None,
    user: Personel = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await get_sending_history_by_user_id(
        session=session,
        user_id=user.id,
        sender_name=sender_username, 
    )

