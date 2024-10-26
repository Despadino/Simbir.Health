
from sqlalchemy import select, update
from app.db.repositories.abstract_repo import AbstractRepository

from app.db.models.models import Appointment


class AppointmentRepository(AbstractRepository):
    model =  Appointment


