from app.db.repositories.users_repo import UserRepository
from app.db.repositories.roles_repo import RolesRepository
from app.db.repositories.employee_roles_repo import EmployeeRolesRepository
from uuid import UUID
from app.settings import settings
from app.db.models.models import Users, Roles, EmployeeRoles
from app.db.schemas.user import *
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import jwt




from app.logger import logger


class authentication:

    def __init__(self, session):
        self.session = session


    async def check_for_doctor(self, UserJWTToken: str):
        user = await self.validate(UserJWTToken)

        roles_Doctor: Roles = await RolesRepository(self.session).get_by_filter_one({"Name": "Doctor"})
        employee_roles_Doctor: EmployeeRoles = await EmployeeRolesRepository(self.session).get_by_filter_one({"user_id": user["user_id"], "roles_id": roles_Doctor.id})

        if employee_roles_Doctor == None:
            raise HTTPException(status_code=401, detail="Недостаточно прав. Нужны права \"Admin\" или \"Manager\"")
        


    async def check_for_admin_or_manager(self, UserJWTToken: str):
        user = await self.validate(UserJWTToken)

        roles_Admin: Roles = await RolesRepository(self.session).get_by_filter_one({"Name": "Admin"})
        employee_roles_Admin: EmployeeRoles = await EmployeeRolesRepository(self.session).get_by_filter_one({"user_id": user["user_id"], "roles_id": roles_Admin.id})

        roles_Manager: Roles = await RolesRepository(self.session).get_by_filter_one({"Name": "Manager"})
        employee_roles_Manager: EmployeeRoles = await EmployeeRolesRepository(self.session).get_by_filter_one({"user_id": user["user_id"], "roles_id": roles_Manager.id})

        if employee_roles_Admin == None and employee_roles_Manager == None:
            raise HTTPException(status_code=401, detail="Недостаточно прав. Нужны права \"Admin\" или \"Manager\"")


    async def check_for_admin_or_manager_or_doctor(self, UserJWTToken: str):
        user = await self.validate(UserJWTToken)

        roles_Admin: Roles = await RolesRepository(self.session).get_by_filter_one({"Name": "Admin"})
        employee_roles_Admin: EmployeeRoles = await EmployeeRolesRepository(self.session).get_by_filter_one({"user_id": user["user_id"], "roles_id": roles_Admin.id})

        roles_Manager: Roles = await RolesRepository(self.session).get_by_filter_one({"Name": "Manager"})
        employee_roles_Manager: EmployeeRoles = await EmployeeRolesRepository(self.session).get_by_filter_one({"user_id": user["user_id"], "roles_id": roles_Manager.id})

        roles_Doctor: Roles = await RolesRepository(self.session).get_by_filter_one({"Name": "Manager"})
        employee_roles_Doctor: EmployeeRoles = await EmployeeRolesRepository(self.session).get_by_filter_one({"user_id": user["user_id"], "roles_id": roles_Doctor.id})


        if employee_roles_Admin == None and employee_roles_Manager == None and employee_roles_Doctor == None:
            raise HTTPException(status_code=401, detail="Недостаточно прав. Нужны права \"Admin\" или \"Manager\"")




    async def check_for_admin(self, UserJWTToken: str):
        user = await self.validate(UserJWTToken)
        roles: Roles = await RolesRepository(self.session).get_by_filter_one({"Name": "Admin"})
        employee_roles: EmployeeRoles = await EmployeeRolesRepository(self.session).get_by_filter_one({"user_id": user["user_id"], "roles_id": roles.id})
        if employee_roles == None:
            raise HTTPException(status_code=401, detail="Недостаточно прав. Нужны права \"Admin\"")



    async def validate(self, token: str):
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
        




    async def get_role(self, token: str):
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
            
            return {"user_id": user_id, "role": await EmployeeRolesRepository(self.session).get_by_filter({"user_id": user_id})}
        
        except jwt.JWTError:
            logger.error("JWT decoding error")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен. Нужно выпустить новый")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")