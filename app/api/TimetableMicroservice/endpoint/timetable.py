import asyncio
from fastapi import APIRouter, Depends, HTTPException, Header, Response, Request

from app.logger import logger
from app.db.db import get_session

from app.db.schemas.user import *
from app.db.models.models import Users
from app.api.TimetableMicroservice.services.TimetableServices import TimetableServices
from app.api.authentication import authentication
from app.logger import logger

router = APIRouter(prefix="/api/Timetable", tags=["Timetable"])


@router.post("")
async def timetable(data: TimetableData, request: Request, session = Depends(get_session)):
    await authentication(session).check_for_admin(request.cookies.get("UserJWTToken"))
    return await TimetableServices(session).create_timetable(data)


@router.put("/{id}")
async def timetable(data: TimetableData, id: str, request: Request, session = Depends(get_session)):
    await authentication(session).check_for_admin(request.cookies.get("UserJWTToken"))
    return await TimetableServices(session).upgrade_timetable(id, data)




@router.delete("/{id}")
async def timetable(id: str, request: Request, session = Depends(get_session)):
    await authentication(session).check_for_admin(request.cookies.get("UserJWTToken"))
    return await TimetableServices(session).delete_by_id(id)


@router.delete("/Doctor/{id}")
async def timetable(id: str, request: Request, session = Depends(get_session)):
    await authentication(session).check_for_admin(request.cookies.get("UserJWTToken"))
    return await TimetableServices(session).delete_by_id_doctor(id)


@router.delete("/Hospital/{id}")
async def timetable(id: str, request: Request, session = Depends(get_session)):
    await authentication(session).check_for_admin(request.cookies.get("UserJWTToken"))
    return await TimetableServices(session).delete_by_id_hospital(id)




@router.get("/Hospital/{id}")
async def timetable(id: str, request: Request, from_datetime: str = Header(None),to_datetime: str = Header(None),session = Depends(get_session)):
    await authentication(session).validate(request.cookies.get("UserJWTToken"))
    return await TimetableServices(session).get_timetable_by_datetime_range_hospital(id, from_datetime, to_datetime)


@router.get("/Doctor/{id}")
async def timetable(id: str, request: Request, from_datetime: str = Header(None),to_datetime: str = Header(None),session = Depends(get_session)):
    await authentication(session).validate(request.cookies.get("UserJWTToken"))
    return await TimetableServices(session).get_timetable_by_datetime_range_doctor(id, from_datetime, to_datetime)


@router.get("/Hospital/{id}/Room/{room}")
async def timetable(id: str, room: str, request: Request, from_datetime: str = Header(None),to_datetime: str = Header(None),session = Depends(get_session)):
    await authentication(session).check_for_admin_or_manager_or_doctor(request.cookies.get("UserJWTToken"))
    return await TimetableServices(session).get_timetable_by_datetime_range_room(id, room, from_datetime, to_datetime)



@router.get("/{id}/Appointments")
async def timetable(id: str, request: Request, from_datetime: str = Header(None),to_datetime: str = Header(None), session = Depends(get_session)):
    await authentication(session).validate(request.cookies.get("UserJWTToken"))
    return await TimetableServices(session).get_appointment(id, from_datetime, to_datetime)


@router.post("/{id}/Appointments")
async def timetable(id: str, time: datetime, request: Request, session = Depends(get_session)):
    user: Users = await authentication(session).validate(request.cookies.get("UserJWTToken"))
    data = AppointmentData(timetable_id=id, time=time.replace(tzinfo=None), user_id=user['user_id'])
    return await TimetableServices(session).create_appointment(data)


