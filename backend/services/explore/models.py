import uuid
from datetime import datetime

from services.portfolio.models import BaseResponseModelWithConfig, PortfolioImage

class PublicPortfolio(BaseResponseModelWithConfig):
    id: uuid.UUID
    user_id: uuid.UUID
    description: str
    commission_slots: int
    created_at: datetime
    updated_at: datetime
    images: list[PortfolioImage]


class PublicPortfolioPage(BaseResponseModelWithConfig):
    items: list[PublicPortfolio]
    page: int
    page_size: int
    total: int
    has_next: bool
