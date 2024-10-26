from app.api.AccountMicroservice.services.AuthenticationServices import AuthenticationServices
from app.db.repositories.users_repo import UserRepository
from app.db.repositories.roles_repo import RolesRepository
from app.db.repositories.employee_roles_repo import EmployeeRolesRepository
from app.db.repositories.hospitals_repo import HospitalsRepository
from app.db.repositories.rooms_repo import RoomsRepository

from fastapi import HTTPException
from uuid import UUID

from app.settings import settings
from app.db.models.models import Users, Roles, EmployeeRoles, Hospitals, Rooms
from app.logger import logger


from app.db.schemas.user import *
class HospitalsServices:

    def __init__(self, session):
        self.session = session


    async def get_hospitals_by_filter(self, count, from_):
        return await HospitalsRepository(self.session).get_all_paginated(from_, count)
    
    async def get_hospitals_by_id(self, id):
        return await HospitalsRepository(self.session).get_by_id(id)
    
    async def delete_hospitals_by_id(self, id):
        delete_data = DeletedUser(is_deleted=True)
        return await HospitalsRepository(self.session).update_one(id, delete_data)
    
    async def get_rooms_by_hospitals_id(self, id):
        filter = {"hospitals_id": id}
        return await RoomsRepository(self.session).get_by_filter(filter)
    

    async def create_hospitals(self, data: CreateOrUpgradeHospitalData):
        data_new_hospital: Hospitals = await HospitalsRepository(self.session).create(HospitalData(name=data.name, address=data.address, contactPhone=data.contactPhone))
        for name_room in data.rooms:
            await RoomsRepository(self.session).create(CreateOrUpgradeRoomsData(name=name_room, hospitals_id=str(data_new_hospital.id)))
        await HospitalsRepository(self.session).commit()



    async def upgrade_hospitals_and_rooms_by_user_id(self, id, data: CreateOrUpgradeHospitalData):
        if await HospitalsRepository(self.session).get_by_id(id) == None:
            raise HTTPException(status_code=401, detail="Нет такой больници")

        await HospitalsRepository(self.session).update_one(id,HospitalData(name=data.name, address=data.address, contactPhone=data.contactPhone))
        
        old_rooms: list[Rooms] = await RoomsRepository(self.session).get_by_filter({"hospitals_id": id})
    
        old_names = {item.name for item in old_rooms}
        new_names = set(data.rooms)
        to_deletes = old_names - new_names
        to_adds = new_names - old_names

        for to_delete_name in to_deletes:
            delete_data = CreateOrUpgradeRoomsData(name=to_delete_name, hospitals_id=id)
            await RoomsRepository(self.session).delete_by_filter(**delete_data.model_dump())



        for to_add in to_adds:
            await RoomsRepository(self.session).create(CreateOrUpgradeRoomsData(name=to_add, hospitals_id=id))
        
        
        await HospitalsRepository(self.session).commit()
        