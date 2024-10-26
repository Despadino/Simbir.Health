from fastapi import Depends, FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from app.settings import settings
from .routers import api_router
from sqlalchemy.exc import IntegrityError
from app.logger import logger

logger.critical("Start AccountMicroservice")


app = FastAPI(
    title="Account microservice", 
    version="1.0.0",
    root_path="/account-microservice"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
