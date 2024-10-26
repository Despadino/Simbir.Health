from fastapi.routing import APIRouter

from .endpoint.history import router  

api_router = APIRouter()

api_router.include_router(router)

