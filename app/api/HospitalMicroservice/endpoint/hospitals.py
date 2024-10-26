import asyncio
from fastapi import APIRouter, Depends, HTTPException, Header, Response, Request

from app.logger import logger
from app.db.db import get_session

from app.db.schemas.user import *
from app.db.models.models import Users
from app.api.HospitalMicroservice.services.HospitalsServices import HospitalsServices
from app.api.authentication import authentication
from app.logger import logger

router = APIRouter(prefix="/api/Hospitals", tags=["Hospitals"])


@router.get("")
async def hospitals(request: Request,count: int = Header(None), from_: int = Header(None), session = Depends(get_session)):
    await authentication(session).validate(request.cookies.get("UserJWTToken"))
    return await HospitalsServices(session).get_hospitals_by_filter(count,from_)


@router.get("{id}")
async def hospitals(request: Request, id: str, session = Depends(get_session)):
    await authentication(session).validate(request.cookies.get("UserJWTToken"))
    return await HospitalsServices(session).get_hospitals_by_id(id)


@router.get("{id}/Rooms")
async def hospitals(request: Request, id: str, session = Depends(get_session)):
    await authentication(session).validate(request.cookies.get("UserJWTToken"))
    return await HospitalsServices(session).get_rooms_by_hospitals_id(id)



@router.post("")
async def hospitals(data: CreateOrUpgradeHospitalData, request: Request, session = Depends(get_session)):
    await authentication(session).check_for_admin(request.cookies.get("UserJWTToken"))
    return await HospitalsServices(session).create_hospitals(data)


@router.put("{id}")
async def hospitals(data: CreateOrUpgradeHospitalData, request: Request, id: str, session = Depends(get_session)):
    await authentication(session).check_for_admin(request.cookies.get("UserJWTToken"))
    return await HospitalsServices(session).upgrade_hospitals_and_rooms_by_user_id(id, data)




@router.delete("{id}")
async def hospitals(request: Request, id: str, session = Depends(get_session)):
    await authentication(session).check_for_admin(request.cookies.get("UserJWTToken"))
    return await HospitalsServices(session).delete_hospitals_by_id(id)