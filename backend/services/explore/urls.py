from fastapi import APIRouter, Depends, HTTPException, status, Query
from database import DbSession

from middleware.auth import get_current_user
from services.explore.models import PublicPortfolioPage
from services.explore.query_functions import get_public_portfolios_qf
from sqlalchemy import text

router = APIRouter()


@router.get(
    "/portfolios",
    response_model=PublicPortfolioPage,
    status_code=status.HTTP_200_OK,
)
def get_public_portfolios(
    db: DbSession,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100, alias="pageSize"),
):
    return get_public_portfolios_qf(
        db=db,
        page=page,
        page_size=page_size,
    )
