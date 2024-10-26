from sqlalchemy import select, update
from app.db.repositories.abstract_repo import AbstractRepository

from app.db.models.models import Hospitals


class HospitalsRepository(AbstractRepository):
    model =  Hospitals


