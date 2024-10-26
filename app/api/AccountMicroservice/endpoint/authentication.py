import asyncio
from fastapi import APIRouter, Depends, HTTPException, Header, Response

from app.logger import logger
from app.db.db import get_session

from app.db.schemas.user import *
from app.api.AccountMicroservice.services.AuthenticationServices import AuthenticationServices
router = APIRouter(prefix="/api/Authentication", tags=["Authentication"])

@router.post("/SignUp") 
async def authentication(data: UserData,  session = Depends(get_session)):
    return await AuthenticationServices(session).create_user(data)
        

@router.post("/SignIn", response_model=UserJWTToken)
async def authentication(data: AuthenticationsUser, response: Response, session = Depends(get_session)):
    token: UserJWTToken = await AuthenticationServices(session).sign_in(data)
    response.set_cookie(key="UserJWTToken", value=token.UserJWTToken)
    return token


@router.put("/SignOut")
async def authentication(response: Response):
    response.delete_cookie(key="UserJWTToken")
    return {"detail": "Вышли из акаунта"}


@router.get("/Validate")
async def authentication(accessToken: UserJWTToken = Header(None), session = Depends(get_session)):
    return await AuthenticationServices(session).validate(accessToken.UserJWTToken)
        

@router.post("/Refresh")
async def authentication(data: UserJWTToken, response: Response, session = Depends(get_session),):
    token: UserJWTToken = await AuthenticationServices(session).refresh_tokens(data.UserJWTToken)
    response.set_cookie(key="UserJWTToken", value=token.UserJWTToken)
    return token