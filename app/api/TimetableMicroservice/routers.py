from fastapi.routing import APIRouter

from .endpoint.timetable import router as timetable 
from .endpoint.appointment import router as appointment 

api_router = APIRouter()

api_router.include_router(timetable)
api_router.include_router(appointment)

