from app.db.repositories.users_repo import UserRepository
from app.db.repositories.roles_repo import RolesRepository
from app.db.repositories.employee_roles_repo import EmployeeRolesRepository

from fastapi import HTTPException
from uuid import UUID

from app.settings import settings
from app.db.models.models import Users, Roles, EmployeeRoles
from app.logger import logger


from app.api.AccountMicroservice.services.AuthenticationServices import AuthenticationServices
from app.db.schemas.user import *
class AccountsServices:

    def __init__(self, session):
        self.session = session


    async def create_employee_roles(self, roles_data, user_id):
            for role in roles_data:
                roles: Roles = await RolesRepository(self.session).get_by_filter_one({"Name": role})
                if roles is None:
                    raise HTTPException(status_code=404, detail=f"Не найдена роль {role}")
                new_employee_roles = EmployeeRolesModel(user_id=str(user_id), roles_id=str(roles.id))
                await EmployeeRolesRepository(self.session).create(new_employee_roles)

            await EmployeeRolesRepository(self.session).commit()


    async def check_for_admin(self, UserJWTToken: str):
        user = await AuthenticationServices(self.session).validate(UserJWTToken)
        roles: Roles = await RolesRepository(self.session).get_by_filter_one({"Name": "Admin"})
        employee_roles: EmployeeRoles = await EmployeeRolesRepository(self.session).get_by_filter_one({"user_id": user["user_id"], "roles_id": roles.id})
        if employee_roles == None:
            raise HTTPException(status_code=401, detail="Недостаточно прав. Нужны права \"Admin\"")


    


    async def get_user_by_UserJWTToken(self, UserJWTToken: str):
        user = await AuthenticationServices(self.session).validate(UserJWTToken)
        return await UserRepository(self.session).get_by_filter_one({"id": user["user_id"]})
    


    async def upgrade_all_role_by_user_id(self, id, roles):
        for role in roles:
                rol: Roles = await RolesRepository(self.session).get_by_filter_one({"Name": role})
                if rol is None:
                    raise HTTPException(status_code=404, detail=f"Не найдена роль {role}")

        role_user = await EmployeeRolesRepository(self.session).get_by_filter_with_roles(id)
        need_add = []
        need_delete = []
        db_roles_set = {role['name'] for role in role_user}
        incoming_roles_set = set(roles)
        roles_to_add = incoming_roles_set - db_roles_set
        need_add = [role for role in roles if role in roles_to_add]
        roles_to_delete = db_roles_set - incoming_roles_set
        need_delete = [role for role in role_user if role['name'] in roles_to_delete]


        await self.create_employee_roles(need_add, id)

        for need_delet in need_delete:
            await EmployeeRolesRepository(self.session).delete_by_id(need_delet["id"])
        await EmployeeRolesRepository(self.session).commit()
        

    async def upgrade_user_by_id(self, id: str, data):
        data = await UserRepository(self.session).update_one(id, data)
        if data == None:
            raise HTTPException(status_code=404, detail="Пользователь с таким id не найден")
        await UserRepository(self.session).commit()
        return data


    async def upgrade_user_by_UserJWTToken(self, UserJWTToken: str, data):
        user = await AuthenticationServices(self.session).validate(UserJWTToken)
        data = await UserRepository(self.session).update_one(user["user_id"], data)
        await UserRepository(self.session).commit()
        return data
    

    async def get_user_by_filter(self, count, from_):
        return await UserRepository(self.session).get_all_paginated(from_, count)
    


    async def delete_user(self, id):
        delete_data = DeletedUser(is_deleted=True)
        data = await UserRepository(self.session).update_one(id, delete_data)
        await UserRepository(self.session).commit()
        if data is None:
            raise HTTPException(status_code=404, detail="Пользователь с таким id не найден")
        return data
