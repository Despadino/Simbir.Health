from app.db.repositories.users_repo import UserRepository
from fastapi import HTTPException, status
from uuid import UUID
from datetime import datetime, timedelta
from jose import jwt

from app.settings import settings

from app.db.models.models import Users
from app.db.schemas.user import *
from app.logger import logger


class AuthenticationServices:

    def __init__(self, session):
        self.session = session
        

    async def get_user_by_username(self, username: str):
        """Получение пользователя по username."""
        return await UserRepository(self.session).get_by_filter_one({"username": username})
    

    async def create_jwt_token(self, data: dict):
        """Создание JWT токена."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return UserJWTToken(UserJWTToken=encoded_jwt)
    
    
    async def create_new_user(self, data: UserData):
        existing_user = await self.get_user_by_username(data.username)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь с таким username уже существует")
        user: Users = await UserRepository(self.session).create(data)
        await UserRepository(self.session).commit()
        return user


    async def create_user(self, data: UserData):
        """Создание нового пользователя."""
        existing_user = await self.get_user_by_username(data.username)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь с таким username уже существует")
        
        user: Users = await UserRepository(self.session).create(data)
        await UserRepository(self.session).commit()
        return await self.create_jwt_token({"id": str(user.id)})


    async def sign_in(self, data: AuthenticationsUser):
        """Аутентификация пользователя."""
        find_user: Users = await self.get_user_by_username(data.username)
        if find_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь с таким логином и паролем не найден")
        
        return await self.create_jwt_token({"id": str(find_user.id)})


    async def validate(self, token: str):
        """Проверка валидности JWT токена."""
        if token == None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Вы не авторизированы")
        try:
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if decoded_data.get("exp") and datetime.utcfromtimestamp(decoded_data["exp"]) < datetime.utcnow():
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Срок действия токена истек")
            
            user_id = decoded_data.get("id")
            if not user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не содержит необходимых данных")
            
            find_user: Users = await UserRepository(self.session).get_by_filter_one({"id": user_id})
            if find_user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
            
            return {"status": "Токен действителен", "user_id": user_id}
        
        except jwt.JWTError:
            logger.error("JWT decoding error")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен. Нужно выпустить новый")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")
        

    async def refresh_tokens(self, refresh_token: str):
        """Обновление JWT токена с использованием refresh токена."""
        try:
            decoded_data = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if decoded_data.get("exp") and datetime.utcfromtimestamp(decoded_data["exp"]) < datetime.utcnow():
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Срок действия refresh токена истек")
            
            user_id = decoded_data.get("id")
            if not user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh токен не содержит необходимых данных")
            
            find_user: Users = await UserRepository(self.session).get_by_filter_one({"id": user_id})
            if find_user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
            
            new_access_token = await self.create_jwt_token({"id": str(find_user.id)})
            
            return new_access_token
        
        except jwt.JWTError:
            logger.error("JWT decoding error")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный refresh токен")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")