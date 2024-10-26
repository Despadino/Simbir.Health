import asyncio
from fastapi import APIRouter, Depends, HTTPException, Header, Response, Request

from app.logger import logger
from app.db.db import get_session

from app.db.schemas.user import *
from app.db.models.models import Users
from app.api.DocumentMicroservice.services.HistoryServices import HistoryServices
from app.api.authentication import authentication
from app.logger import logger

router = APIRouter(prefix="/api/History", tags=["History"])


@router.get("/Account/{id}")
async def history(id: str, request: Request, session = Depends(get_session)):
    return await HistoryServices(session).get_history_account(id, request.cookies.get("UserJWTToken"))


@router.get("/{id}")
async def history(id: str, request: Request, session = Depends(get_session)):
    return await HistoryServices(session).get_history_account(id, request.cookies.get("UserJWTToken"))


@router.post("")
async def history(request: Request, session = Depends(get_session)):
    return "API не доделано"


@router.put("/{id}")
async def history(id: str, request: Request, session = Depends(get_session)):
    return "API не доделано"