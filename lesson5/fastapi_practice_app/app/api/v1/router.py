from app.api.v1.health import router as health_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.users import router as users_router
from fastapi import APIRouter

api_router = APIRouter()

# Aggregate all v1 routers under one entrypoint.
api_router.include_router(health_router)
api_router.include_router(users_router)
api_router.include_router(tasks_router)
