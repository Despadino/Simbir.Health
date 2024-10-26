from fastapi.routing import APIRouter

from .endpoint.authentication import router as router_authentication
from .endpoint.accounts import router as router_accounts
from .endpoint.doctors import router as router_doctors

api_router = APIRouter()

api_router.include_router(router_authentication)
api_router.include_router(router_accounts)
api_router.include_router(router_doctors)
