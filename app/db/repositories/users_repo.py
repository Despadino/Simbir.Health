from sqlalchemy import select, update, text, or_
from app.db.repositories.abstract_repo import AbstractRepository

from app.db.models.models import Users


class UserRepository(AbstractRepository):
    model =  Users


    

    async def get_by_ids(self, user_ids: list):
        query = select(self.model).filter(Users.id.in_(user_ids))
        result = await self._session.execute(query)
        return result.scalars().all()
    
    
    async def get_by_ids_with_filter(self, user_ids: list, from_: int, count: int, nameFilter: str = None):
        query = select(Users).filter(Users.id.in_(user_ids)).offset(from_).limit(count)
        
        if nameFilter:
            query = query.filter(or_(
                Users.firstName.ilike(f"%{nameFilter}%"),
                Users.lastName.ilike(f"%{nameFilter}%"),
                Users.username.ilike(f"%{nameFilter}%")
            ))
        
        result = await self._session.execute(query)
        return result.scalars().all()