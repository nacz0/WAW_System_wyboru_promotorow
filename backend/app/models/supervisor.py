from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base

class Supervisor(Base):
    __tablename__ = "supervisors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(50), nullable=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="supervisor")
    topic_proposals: Mapped[list["TopicProposal"]] = relationship("TopicProposal", back_populates="supervisor")
    preferences: Mapped[list["Preference"]] = relationship("Preference", back_populates="supervisor")
    assignments: Mapped[list["Assignment"]] = relationship("Assignment", back_populates="supervisor")


from app.models.user import User
from app.models.topic_proposal import TopicProposal
from app.models.preference import Preference
from app.models.assignment import Assignment