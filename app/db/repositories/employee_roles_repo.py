from sqlalchemy import select, update, join
from app.db.repositories.abstract_repo import AbstractRepository

from app.db.models.models import EmployeeRoles
from app.db.models.models import Roles


class EmployeeRolesRepository(AbstractRepository):
    model =  EmployeeRoles


    async def get_by_filter_with_roles(self, user_id):
        query = (
            select(EmployeeRoles, Roles)
            .select_from(
                join(EmployeeRoles, Roles, EmployeeRoles.roles_id == Roles.id)
            )
            .filter(EmployeeRoles.user_id == user_id)
        )
        result = await self._session.execute(query)
        rows = result.all()
        return [
            {
                "id": row.EmployeeRoles.id,
                "user_id": row.EmployeeRoles.user_id,
                "name": row.Roles.Name,
            }
            for row in rows
        ]