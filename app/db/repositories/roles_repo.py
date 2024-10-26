from sqlalchemy import select, update
from app.db.repositories.abstract_repo import AbstractRepository

from app.db.models.models import Roles


class RolesRepository(AbstractRepository):
    model =  Roles


