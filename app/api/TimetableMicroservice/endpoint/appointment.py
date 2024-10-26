import asyncio
from fastapi import APIRouter, Depends, HTTPException, Header, Response, Request

from app.logger import logger
from app.db.db import get_session

from app.db.schemas.user import *
from app.db.models.models import Users
from app.api.TimetableMicroservice.services.TimetableServices import TimetableServices
from app.api.authentication import authentication
from app.logger import logger

router = APIRouter(prefix="/api/Appointment", tags=["Appointment"])



@router.delete("/{id}")
async def timetable(id: str, request: Request, session = Depends(get_session)):
    user = await authentication(session).validate(request.cookies.get("UserJWTToken"))
    return await TimetableServices(session).delete_by_id_appointment(id, user["user_id"], request.cookies.get("UserJWTToken"))