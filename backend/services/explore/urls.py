from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from database import DbSession

from middleware.auth import get_current_user
from services.explore.models import PublicPortfolio, PublicPortfolioPage
from services.explore.query_functions import get_public_portfolio_by_id_qf, get_public_portfolios_qf
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
    tags: str | None = Query(default=None),
):
    parsed_tags = (
        [tag.strip() for tag in tags.split(",") if tag.strip()]
        if tags
        else None
    )

    return get_public_portfolios_qf(
        db=db,
        page=page,
        page_size=page_size,
        tags=parsed_tags,
    )


@router.get(
    "/portfolios/{portfolio_id}",
    response_model=PublicPortfolio,
    status_code=status.HTTP_200_OK,
)
def get_public_portfolio_by_id(
    db: DbSession,
    portfolio_id: UUID,
):
    return get_public_portfolio_by_id_qf(
        db=db,
        portfolio_id=portfolio_id,
    )
