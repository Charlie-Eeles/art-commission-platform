from fastapi import APIRouter
from services.health_check.urls import router as health_check_router

router = APIRouter()

router.include_router(health_check_router, prefix="/health-check")
