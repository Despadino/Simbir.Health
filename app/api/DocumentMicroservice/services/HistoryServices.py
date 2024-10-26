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

class HistoryServices:

    def __init__(self, session):
        self.session = session


    async def get_history_account(self, id, jwt):
        user = await authentication(self.session).get_role(jwt)
        appointments = await AppointmentRepository(self.session).get_by_id(id)
        if appointments is None:
            return None
        if id != user["user_id"]:
            await authentication(self.session).check_for_doctor(jwt)
        history = []
        if isinstance(appointments, list):
            for appointment in appointments:
                timetable = await TimetableRepository(self.session).get_by_id(appointment.timetable_id)
                history.append({
                    "date": appointment.time,
                    "pacientId": appointment.user_id,
                    "hospitalId": timetable.hospital_id,
                    "doctorId": timetable.doctor_id,
                    "room": timetable.room,
                })
        else:
            timetable = await TimetableRepository(self.session).get_by_id(appointments.timetable_id)
            history.append({
                "date": appointments.time,
                "pacientId": appointments.user_id,
                "hospitalId": timetable.hospital_id,
                "doctorId": timetable.doctor_id,
                "room": timetable.room,
            })
        
        return history

