import asyncio
from fastapi import APIRouter, Depends, HTTPException, Header, Response, Request

from app.logger import logger
from app.db.db import get_session

from app.db.schemas.user import *
from app.api.AccountMicroservice.services.AccountsServices import AccountsServices
from app.api.AccountMicroservice.services.AuthenticationServices import AuthenticationServices
from app.db.models.models import Users

router = APIRouter(prefix="/api/Accounts", tags=["Accounts"])

@router.get("/Me")
async def accounts(request: Request, session = Depends(get_session)):
    return await AccountsServices(session).get_user_by_UserJWTToken(request.cookies.get("UserJWTToken"))

@router.put("/Update")
async def accounts(data: Upgradeuser, request: Request, session = Depends(get_session)):
    return await AccountsServices(session).upgrade_user_by_UserJWTToken(request.cookies.get("UserJWTToken"), data)


@router.get("")
async def accounts(request: Request, count: int = Header(None), from_: int = Header(None), session = Depends(get_session)):
    await AccountsServices(session).check_for_admin(request.cookies.get("UserJWTToken"))
    return await AccountsServices(session).get_user_by_filter(count,from_)
        

@router.post("")
async def accounts(data: UpgradeRole, request: Request, session = Depends(get_session)):
    await AccountsServices(session).check_for_admin(request.cookies.get("UserJWTToken"))
    new_user = UserData(
        lastName=data.lastName,
        firstName=data.firstName,
        username=data.username,
        password=data.password
    )
    user: Users = await AuthenticationServices(session).create_new_user(new_user)
    await AccountsServices(session).create_employee_roles(data.roles, user.id)

    
        

@router.put("/{id}")
async def accounts(id: str, data: UpgradeRole, request: Request, session = Depends(get_session)):
    await AccountsServices(session).check_for_admin(request.cookies.get("UserJWTToken"))
    user = UserData(
        lastName=data.lastName,
        firstName=data.firstName,
        username=data.username,
        password=data.password
    )
    return await AccountsServices(session).upgrade_all_role_by_user_id(id, data.roles)




@router.delete("/{id}")
async def accounts(id: str, request: Request, session = Depends(get_session)):
    await AccountsServices(session).check_for_admin(request.cookies.get("UserJWTToken"))
    return await AccountsServices(session).delete_user(id)
        