import enum
from datetime import datetime

from sqlalchemy import String, DateTime, Enum, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base

class RoundStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    DRAFT = "draft"
    COMPLETED = "completed"


class SelectionRound(Base):
    __tablename__ = "selection_rounds"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[RoundStatus] = mapped_column(Enum(RoundStatus), nullable=False, default=RoundStatus.DRAFT)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    preferences: Mapped[list["Preference"]] = relationship("Preference", back_populates="selection_round")
    assignments: Mapped[list["Assignment"]] = relationship("Assignment", back_populates="selection_round")

from app.models.preference import Preference
from app.models.assignment import Assignment
