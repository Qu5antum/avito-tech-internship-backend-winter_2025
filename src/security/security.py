from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from src.config.settings import settings
import jwt
import datetime
from src.database.db import get_session, AsyncSession
from src.models.models import Personel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

async def create_jwt_token(data):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def auth_user(credents: OAuth2PasswordRequestForm, session: AsyncSession = Depends(get_session)):
    query = select(Personel).where(Personel.username == credents.username)
    result = await session.execute(query)
    personel = result.scalar_one_or_none()

    if not personel:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден."
        )
    
    if personel.password != credents.password:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Неавторизован."
        )
    
    token = await create_jwt_token({"sub": str(personel.id)})
    return {"access_token": token,
            "token_type": "bearer"}
    

async def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        playload = jwt.decode(token, settings.SECRET_KEY, algorithms = [settings.ALGORITHM])
        user_id: int = playload.get("sub")
        if user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Недействительный токен.")
        return int(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Срок действия токена истек.")
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Недействительный токен.")
    

async def get_current_user(user_id: int = Depends(get_user_from_token), session: AsyncSession = Depends(get_session)):
    user = await session.get(Personel, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Пользователь не найден.")
    return user
                           