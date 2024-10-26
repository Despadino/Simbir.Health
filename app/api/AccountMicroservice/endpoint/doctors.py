import asyncio
from fastapi import APIRouter, Depends, HTTPException, Header, Request

from app.logger import logger
from app.db.db import get_session

from app.db.schemas.user import *
from app.api.AccountMicroservice.services.AuthenticationServices import AuthenticationServices
from app.api.AccountMicroservice.services.DoctorsServices import DoctorsServices
router = APIRouter(prefix="/api/Doctors", tags=["Doctors"])


@router.get("")
async def doctors(request: Request, nameFilter: str = Header(None), from_: int = Header(None), count: int = Header(None), session = Depends(get_session)):
    await AuthenticationServices(session).validate(request.cookies.get("UserJWTToken"))
    return await DoctorsServices(session).get_docktor_by_filter(from_, count, nameFilter)
        

@router.get("/{id}")
async def doctors(request: Request, id: str, session = Depends(get_session)):
    await AuthenticationServices(session).validate(request.cookies.get("UserJWTToken"))
    return await DoctorsServices(session).get_docktor_by_id(id)


