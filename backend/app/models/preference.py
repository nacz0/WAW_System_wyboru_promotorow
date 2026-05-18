from sqlalchemy import ForeignKey, Integer, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base

class Preference(Base):
    __tablename__ = "preferences"
    __tableargs__ = (
        UniqueConstraint("selection_round_id", "student_id", "priority", name="uq_student_round_priority"),
        UniqueConstraint("selection_round_id", "team_id", "priority", name="uq_team_round_priority"),
        CheckConstraint("priority >= 1 AND priority <= 3", name="ck_priority_range"),
        CheckConstraint(
            "(student_id IS NOT NULL AND team_id IS NULL) OR (student_id IS NULL AND team_id IS NOT NULL)",
            name="ck_student_or_team",
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
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    supervisor_id: Mapped[int] = mapped_column(
        ForeignKey("supervisors.id", ondelete="CASCADE"), nullable=False, index=True
    )

    selection_round: Mapped["SelectionRound"] = relationship("SelectionRound", back_populates="preferences")
    student: Mapped["Student | None"] = relationship("Student", back_populates="preferences")
    team: Mapped["Team | None"] = relationship("Team", back_populates="preferences")
    supervisor: Mapped["Supervisor"] = relationship("Supervisor", back_populates="preferences")

from app.models.selection_round import SelectionRound
from app.models.student import Student
from app.models.team import Team
from app.models.supervisor import Supervisor