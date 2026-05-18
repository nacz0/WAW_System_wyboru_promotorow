from decimal import Decimal

from sqlalchemy import String, ForeignKey, Numeric, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    album_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    average_grade: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False, default=Decimal("0.00"))
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="student")
    team: Mapped["Team | None"] = relationship("Team", back_populates="members", foreign_keys=[team_id])
    led_team: Mapped["Team | None"] = relationship("Team", back_populates="leader", foreign_keys="[Team.leader_student_id]", uselist=False)
    preferences: Mapped[list["Preference"]] = relationship("Preference", back_populates="student")
    assignments: Mapped[list["Assignment"]] = relationship("Assignment", back_populates="student")


from app.models.user import User
from app.models.team import Team
from app.models.preference import Preference
from app.models.assignment import Assignment