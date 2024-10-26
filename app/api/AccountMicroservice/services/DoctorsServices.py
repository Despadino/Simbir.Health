from pydantic import BaseModel
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

class IDRolesModel(BaseModel):
    roles_id: str

class DoctorsServices:

    def __init__(self, session):
        self.session = session

    async def get_docktor_by_filter(self, from_: int, count: int, nameFilter: str = None):
        rol: Roles = await RolesRepository(self.session).get_by_filter_one({"Name": "Doctor"})
        if rol is None:
            raise HTTPException(status_code=404, detail=f"Не найдена роль Doctor")
        employee_roles = IDRolesModel(roles_id=str(rol.id))
        employee_roles_dict = employee_roles.dict()
        doctor_employee_roles = await EmployeeRolesRepository(self.session).get_by_filter(employee_roles_dict)
        user_ids = [er.user_id for er in doctor_employee_roles]
        doctors = await UserRepository(self.session).get_by_ids_with_filter(user_ids, from_, count, nameFilter)
        return doctors
    

    async def get_docktor_by_id(self, id):
        rol: Roles = await RolesRepository(self.session).get_by_filter_one({"Name": "Doctor"})
        if rol is None:
            raise HTTPException(status_code=404, detail=f"Не найдена роль Doctor")
        
        doctor = await EmployeeRolesRepository(self.session).get_by_filter_one({"user_id": id, "roles_id": rol.id})
        if doctor == None:
            raise HTTPException(status_code=404, detail=f"Не найдена Doctor с таким id")

        return await UserRepository(self.session).get_by_id(id)