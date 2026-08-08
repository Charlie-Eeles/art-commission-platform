import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseRequestModelWithConfig(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=False,
    )


class BaseResponseModelWithConfig(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=False,
    )


class PortfolioImage(BaseResponseModelWithConfig):
    id: uuid.UUID
    art_name: str
    image_url: str
    upload_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UpdatePortfolioImageRequest(BaseRequestModelWithConfig):
    art_name: str


class PortfolioSettingsRequest(BaseRequestModelWithConfig):
    description: str
    is_public: bool
    commission_slots: int


class PortfolioSettings(BaseResponseModelWithConfig):
    id: uuid.UUID
    user_id: uuid.UUID
    description: str
    is_public: bool
    commission_slots: int
    created_at: datetime
    updated_at: datetime

class PortfolioTag(BaseResponseModelWithConfig):
    id: uuid.UUID
    name: str
    created_at: datetime
