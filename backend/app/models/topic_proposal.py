from sqlalchemy import String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base

class TopicProposal(Base):
    __tablename__ = "topic_proposals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    supervisor_id: Mapped[int] = mapped_column(ForeignKey("supervisors.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    supervisor: Mapped["Supervisor"] = relationship("Supervisor", back_populates="topic_proposals")

from app.models.supervisor import Supervisor