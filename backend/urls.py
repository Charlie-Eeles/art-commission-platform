from fastapi import APIRouter

from services.accounts.urls import router as accounts_router
from services.health_check.urls import router as health_check_router

router = APIRouter()

router.include_router(accounts_router, prefix="/accounts")
router.include_router(health_check_router, prefix="/health-check")
