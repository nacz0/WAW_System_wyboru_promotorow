from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    leader_student_id: Mapped[int | None] = mapped_column(
        ForeignKey("students.id", ondelete="SET NULL", use_alter=True), nullable=True, unique=True
    )
    assigned_supervisor_id: Mapped[int | None] = mapped_column(
        ForeignKey("supervisors.id", ondelete="SET NULL"), nullable=True
    )
    max_size: Mapped[int] = mapped_column(Integer, nullable=False, default=5)

    leader: Mapped["Student | None"] = relationship("Student", back_populates="led_team", foreign_keys=[leader_student_id])
    members: Mapped[list["Student"]] = relationship("Student", back_populates="team", foreign_keys="[Student.team_id]")
    assigned_supervisor: Mapped["Supervisor | None"] = relationship("Supervisor", foreign_keys=[assigned_supervisor_id])
    preferences: Mapped[list["Preference"]] = relationship("Preference", back_populates="team")
    assignments: Mapped[list["Assignment"]] = relationship("Assignment", back_populates="team")

from app.models.student import Student
from app.models.supervisor import Supervisor
from app.models.preference import Preference
from app.models.assignment import Assignment