import uuid
from datetime import datetime

from pydantic import BaseModel

class PortfolioImage(BaseModel):
    id: uuid.UUID
    art_name: str
    image_url: str
    upload_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UpdatePortfolioImageRequest(BaseModel):
    art_name: str
