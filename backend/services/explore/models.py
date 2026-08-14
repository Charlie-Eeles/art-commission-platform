import uuid
from datetime import datetime

from services.portfolio.models import (
    BaseResponseModelWithConfig,
    PortfolioImage,
    PortfolioTag,
)


class PublicPortfolio(BaseResponseModelWithConfig):
    id: uuid.UUID
    user_id: uuid.UUID
    description: str
    commission_slots: int
    open_commission_slots: int
    created_at: datetime
    updated_at: datetime
    images: list[PortfolioImage]
    tags: list[PortfolioTag]


class PublicPortfolioPage(BaseResponseModelWithConfig):
    items: list[PublicPortfolio]
    page: int
    page_size: int
    total: int
    has_next: bool
