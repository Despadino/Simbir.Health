from sqlalchemy import select, update
from app.db.repositories.abstract_repo import AbstractRepository
from dateutil import parser
from datetime import datetime, timedelta

from app.db.models.models import Timetable


class TimetableRepository(AbstractRepository):
    model =  Timetable



    
    async def get_by_datetime_range_hospital(self, hospital_id: str, from_datetime: str = None, to_datetime: str = None):
            query = select(self.model).where(self.model.hospital_id == hospital_id)

            if from_datetime:
                from_dt = parser.isoparse(from_datetime).replace(tzinfo=None)
                query = query.where(self.model.from_datetime >= from_dt)

            if to_datetime:
                to_dt = parser.isoparse(to_datetime).replace(tzinfo=None)
                query = query.where(self.model.to_datetime <= to_dt)

            result = await self._session.execute(query)
            return result.scalars().all()
    
    
    async def get_by_datetime_range_doctor_id(self, doctor_id: str, from_datetime: str = None, to_datetime: str = None):
            query = select(self.model).where(self.model.doctor_id == doctor_id)

            if from_datetime:
                from_dt = parser.isoparse(from_datetime).replace(tzinfo=None)
                query = query.where(self.model.from_datetime >= from_dt)

            if to_datetime:
                to_dt = parser.isoparse(to_datetime).replace(tzinfo=None)
                query = query.where(self.model.to_datetime <= to_dt)

            result = await self._session.execute(query)
            return result.scalars().all()
    
    async def get_by_datetime_range_room(self, hospital_id: str,  room: str, from_datetime: str = None, to_datetime: str = None):
            query = select(self.model).where(self.model.room == room, self.model.hospital_id == hospital_id)

            if from_datetime:
                from_dt = parser.isoparse(from_datetime).replace(tzinfo=None)
                query = query.where(self.model.from_datetime >= from_dt)

            if to_datetime:
                to_dt = parser.isoparse(to_datetime).replace(tzinfo=None)
                query = query.where(self.model.to_datetime <= to_dt)

            result = await self._session.execute(query)
            return result.scalars().all()
    


