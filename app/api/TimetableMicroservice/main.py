from fastapi import Depends, FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from app.settings import settings
from .routers import api_router
from sqlalchemy.exc import IntegrityError
from app.logger import logger

logger.critical("Start TimetableMicroservice")

app = FastAPI(
    title="Timetable microservice", 
    version="1.0.0",
    root_path="/timetable-microservice"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
