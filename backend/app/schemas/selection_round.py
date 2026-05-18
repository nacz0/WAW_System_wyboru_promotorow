from datetime import datetime
from pydantic import BaseModel, field_validator

from app.models.selection_round import RoundStatus

class SelectionRoundBase(BaseModel):
    name: str
    starts_at: datetime
    ends_at: datetime

    @field_validator("ends_at")
    @classmethod
    def ends_after_starts(cls, v: datetime, info) -> datetime:
        if "starts_at" in info.data and v <= info.data["starts_at"]:
            raise ValueError("ends_at must be after starts_at")
        return v
    
class SelectionRoundCreate(SelectionRoundBase):
    pass

class SelectionRoundUpdate(BaseModel):
    name: str | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    status: RoundStatus | None = None

    @field_validator("ends_at")
    @classmethod
    def ends_after_starts(cls, v: datetime, info) -> datetime:
        if v is not None and "starts_at" in info.data and info.data["starts_at"] is not None and v <= info.data["starts_at"]:
            raise ValueError("ends_at must be after starts_at")
        return v
    
class SelectionRoundRead(SelectionRoundBase):
    id: int
    status: RoundStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }