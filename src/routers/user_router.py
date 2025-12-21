from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.services.create_user import create_new_user
from src.security.security import auth_user
from src.schemas.schemas import UserCreate
from src.database.db import get_session, AsyncSession

router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.post("/register", status_code=status.HTTP_200_OK)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await create_new_user(session, user)
    
    
@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    return await auth_user(user, session)
    


