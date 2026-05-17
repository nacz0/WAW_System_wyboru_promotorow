import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    student = "student"
    supervisor = "supervisor"


class RoundStatus(str, enum.Enum):
    draft = "draft"
    open = "open"
    closed = "closed"
    assigned = "assigned"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, native_enum=False), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    student: Mapped["Student | None"] = relationship(back_populates="user", uselist=False)
    supervisor: Mapped["Supervisor | None"] = relationship(back_populates="user", uselist=False)


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    album_number: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    average_grade: Mapped[float] = mapped_column(Float, nullable=False)

    user: Mapped[User] = relationship(back_populates="student")
    team_memberships: Mapped[list["TeamMember"]] = relationship(back_populates="student", cascade="all, delete-orphan")


class Supervisor(Base):
    __tablename__ = "supervisors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    user: Mapped[User] = relationship(back_populates="supervisor")
    topics: Mapped[list["TopicProposal"]] = relationship(back_populates="supervisor", cascade="all, delete-orphan")


class TopicProposal(Base):
    __tablename__ = "topic_proposals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    supervisor_id: Mapped[int] = mapped_column(ForeignKey("supervisors.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    supervisor: Mapped[Supervisor] = relationship(back_populates="topics")


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    leader_student_id: Mapped[int | None] = mapped_column(ForeignKey("students.id"))
    assigned_supervisor_id: Mapped[int | None] = mapped_column(ForeignKey("supervisors.id"))

    leader: Mapped[Student | None] = relationship(foreign_keys=[leader_student_id])
    assigned_supervisor: Mapped[Supervisor | None] = relationship(foreign_keys=[assigned_supervisor_id])
    members: Mapped[list["TeamMember"]] = relationship(back_populates="team", cascade="all, delete-orphan")


class TeamMember(Base):
    __tablename__ = "team_members"
    __table_args__ = (
        UniqueConstraint("team_id", "student_id", name="uq_team_member"),
        UniqueConstraint("student_id", name="uq_student_single_team"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)

    team: Mapped[Team] = relationship(back_populates="members")
    student: Mapped[Student] = relationship(back_populates="team_memberships")


class SelectionRound(Base):
    __tablename__ = "selection_rounds"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[RoundStatus] = mapped_column(Enum(RoundStatus, native_enum=False), default=RoundStatus.draft, nullable=False)


class Preference(Base):
    __tablename__ = "preferences"
    __table_args__ = (
        UniqueConstraint("selection_round_id", "student_id", "priority", name="uq_student_preference_priority"),
        UniqueConstraint("selection_round_id", "team_id", "priority", name="uq_team_preference_priority"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    selection_round_id: Mapped[int] = mapped_column(ForeignKey("selection_rounds.id"), nullable=False)
    student_id: Mapped[int | None] = mapped_column(ForeignKey("students.id"))
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"))
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    supervisor_id: Mapped[int] = mapped_column(ForeignKey("supervisors.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    selection_round: Mapped[SelectionRound] = relationship()
    student: Mapped[Student | None] = relationship()
    team: Mapped[Team | None] = relationship()
    supervisor: Mapped[Supervisor] = relationship()


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    selection_round_id: Mapped[int] = mapped_column(ForeignKey("selection_rounds.id"), nullable=False)
    student_id: Mapped[int | None] = mapped_column(ForeignKey("students.id"))
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"))
    supervisor_id: Mapped[int] = mapped_column(ForeignKey("supervisors.id"), nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    assignment_source: Mapped[str] = mapped_column(String(50), nullable=False)

    selection_round: Mapped[SelectionRound] = relationship()
    student: Mapped[Student | None] = relationship()
    team: Mapped[Team | None] = relationship()
    supervisor: Mapped[Supervisor] = relationship()
