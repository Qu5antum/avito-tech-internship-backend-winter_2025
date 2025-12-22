from fastapi import APIRouter, status, Depends, HTTPException
from src.services.admin_services import add_merch
from src.database.db import get_session, AsyncSession
from src.schemas.schemas import MerchCreate

router = APIRouter(
    prefix="/admin_panel",
    tags=["admin"]
)

@router.post("/add_merch", status_code=status.HTTP_200_OK)
async def add_new_merch(merch: MerchCreate, session: AsyncSession = Depends(get_session)):
    return await add_merch(session, merch)