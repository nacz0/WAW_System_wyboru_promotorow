from datetime import datetime

from sqlalchemy import ForeignKey, String, DateTime, func, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base

class Assignment(Base):
    __tablename__ = "assignments"
    __tableargs__ = (
        CheckConstraint(
            "(student_id IS NOT NULL AND team_id IS NULL) OR (student_id IS NULL AND team_id IS NOT NULL)",
            name="ck_assignment_student_or_team",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    selection_round_id: Mapped[int] = mapped_column(
        ForeignKey("selection_rounds.id", ondelete="CASCADE"), nullable=False, index=True
    )
    student_id: Mapped[int | None] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=True, index=True
    )
    team_id: Mapped[int | None] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"), nullable=True, index=True
    )
    supervisor_id: Mapped[int] = mapped_column(
        ForeignKey("supervisors.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    assignment_source: Mapped[str] = mapped_column(
        String(255), nullable=False, default="preference_1"
    )

    selection_round: Mapped["SelectionRound"] = relationship("SelectionRound", back_populates="assignments")
    student: Mapped["Student | None"] = relationship("Student", back_populates="assignments")
    team: Mapped["Team | None"] = relationship("Team", back_populates="assignments")
    supervisor: Mapped["Supervisor"] = relationship("Supervisor", back_populates="assignments")

from app.models.selection_round import SelectionRound
from app.models.student import Student
from app.models.team import Team
from app.models.supervisor import Supervisor
