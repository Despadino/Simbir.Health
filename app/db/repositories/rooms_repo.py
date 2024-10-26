
from sqlalchemy import select, update
from app.db.repositories.abstract_repo import AbstractRepository

from app.db.models.models import Rooms


class RoomsRepository(AbstractRepository):
    model =  Rooms


