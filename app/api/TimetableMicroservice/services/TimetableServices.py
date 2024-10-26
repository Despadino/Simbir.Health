from app.api.AccountMicroservice.services.AuthenticationServices import AuthenticationServices
from app.db.repositories.users_repo import UserRepository
from app.db.repositories.roles_repo import RolesRepository
from app.db.repositories.employee_roles_repo import EmployeeRolesRepository
from app.db.repositories.hospitals_repo import HospitalsRepository
from app.db.repositories.rooms_repo import RoomsRepository
from app.db.repositories.timetable_repo import TimetableRepository
from app.db.repositories.appointment_repo import AppointmentRepository

from fastapi import HTTPException
from uuid import UUID

from app.settings import settings
from app.db.models.models import Users, Roles, EmployeeRoles, Hospitals, Rooms, Timetable, Appointment
from app.logger import logger
from datetime import timezone
from app.api.authentication import authentication

from app.db.schemas.user import *
class TimetableServices:

    def __init__(self, session):
        self.session = session


    async def create_timetable(self, data: TimetableData):
        if await UserRepository(self.session).get_by_id(data.doctor_id) == None:
            raise HTTPException(status_code=401, detail=f"Не найден доктор с id {data.doctor_id}")

        if await HospitalsRepository(self.session).get_by_id(data.hospital_id) == None:
            raise HTTPException(status_code=401, detail=f"Не найдена больница с id {data.hospital_id}")
        
        if await RoomsRepository(self.session).get_by_filter((CreateOrUpgradeRoomsData(name=data.room, hospitals_id=data.hospital_id)).dict()) == []:
            raise HTTPException(status_code=401, detail=f"Не найдена комната {data.room} в больнице {data.hospital_id}")

        new_data = await TimetableRepository(self.session).create(data)
        await TimetableRepository(self.session).commit()
        return new_data
    

    async def upgrade_timetable(self, id, data: TimetableData):
        if await UserRepository(self.session).get_by_id(data.doctor_id) == None:
            raise HTTPException(status_code=401, detail=f"Не найден доктор с id {data.doctor_id}")

        if await HospitalsRepository(self.session).get_by_id(data.hospital_id) == None:
            raise HTTPException(status_code=401, detail=f"Не найдена больница с id {data.hospital_id}")
        
        if await RoomsRepository(self.session).get_by_filter((CreateOrUpgradeRoomsData(name=data.room, hospitals_id=data.hospital_id)).dict()) == []:
            raise HTTPException(status_code=401, detail=f"Не найдена комната {data.room} в больнице {data.hospital_id}")

        new_data = await TimetableRepository(self.session).update_one(id, data)
        await TimetableRepository(self.session).commit()
        return new_data


    async def delete_by_id(self, id):
        new_data = await TimetableRepository(self.session).delete_by_id(id)
        await TimetableRepository(self.session).commit()
        return new_data


    async def delete_by_id_doctor(self, id):
        new_data = await TimetableRepository(self.session).delete_by_filter(doctor_id=id)
        await TimetableRepository(self.session).commit()
        return new_data


    async def delete_by_id_hospital(self, id):
        new_data = await TimetableRepository(self.session).delete_by_filter(hospital_id=id)
        await TimetableRepository(self.session).commit()
        return new_data


    async def get_timetable_by_datetime_range_hospital(self, id, from_datetime: str, to_datetime: str):
        return await TimetableRepository(self.session).get_by_datetime_range_hospital(id, from_datetime, to_datetime)
    

    async def get_timetable_by_datetime_range_doctor(self, id, from_datetime: str, to_datetime: str):
        return await TimetableRepository(self.session).get_by_datetime_range_doctor_id(id, from_datetime, to_datetime)
    

    async def get_timetable_by_datetime_range_room(self, hospital_id, room, from_datetime: str, to_datetime: str):
        return await TimetableRepository(self.session).get_by_datetime_range_room(hospital_id, room, from_datetime, to_datetime)
    

    async def create_appointment(self, data: AppointmentData):
        find = await AppointmentRepository(self.session).get_by_filter({"timetable_id": data.timetable_id, "time": data.time})
        if find != []:
            raise HTTPException(status_code=409, detail="Такая запись уже занята")
        
        data_timetable: Timetable = await TimetableRepository(self.session).get_by_id(data.timetable_id)

        if data_timetable.from_datetime > data.time or data_timetable.to_datetime < data.time:
            raise HTTPException(status_code=400, detail="Время записи выходит за пределы периода времени в расписании")

        data_appointment = await AppointmentRepository(self.session).create(data)
        await AppointmentRepository(self.session).commit()
        return data_appointment


    async def get_appointment(self, id, from_datetime=None, to_datetime=None, ):
        data_timetable: Timetable = await TimetableRepository(self.session).get_by_id(id)
        data_appointment: List[Appointment] = await AppointmentRepository(self.session).get_by_filter({"timetable_id": id})

        if not from_datetime:
            from_datetime = data_timetable.from_datetime
        if not to_datetime:
            to_datetime = data_timetable.to_datetime

        # Ensure from_datetime and to_datetime are datetime objects
        if isinstance(from_datetime, str):
            from_datetime = datetime.fromisoformat(from_datetime)
        if isinstance(to_datetime, str):
            to_datetime = datetime.fromisoformat(to_datetime)

        # Ensure data_timetable.from_datetime and data_timetable.to_datetime are datetime objects
        if isinstance(data_timetable.from_datetime, str):
            data_timetable.from_datetime = datetime.fromisoformat(data_timetable.from_datetime)
        if isinstance(data_timetable.to_datetime, str):
            data_timetable.to_datetime = datetime.fromisoformat(data_timetable.to_datetime)

        available_slots = []
        current_time = from_datetime
        
        while current_time.replace(tzinfo=None) < to_datetime.replace(tzinfo=None):
            available_slots.append(current_time.strftime('%Y-%m-%dT%H:%M:%SZ'))
            current_time += timedelta(minutes=30)

        # Convert occupied slots to isoformat strings
        occupied_slots = {appointment.time.strftime('%Y-%m-%dT%H:%M:%SZ') for appointment in data_appointment}

        # Filter out occupied slots from available slots
        free_slots = [slot for slot in available_slots if slot not in occupied_slots]

        return free_slots
    

    async def delete_by_id_appointment(self, id, user_id, jwt):
        no_current_user = True
        find_data: Appointment = await AppointmentRepository(self.session).get_by_id(id)
        if find_data.user_id == user_id: 
            no_current_user = False
        
        if no_current_user:
            await authentication(self.session).check_for_admin_or_manager(jwt)
            


        new_data = await AppointmentRepository(self.session).delete_by_id(id)
        await AppointmentRepository(self.session).commit()
        return new_data
    
