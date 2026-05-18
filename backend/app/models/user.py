import enum
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, Enum, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STUDENT = "student"
    SUPERVISOR = "supervisor"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    student: Mapped["Student"] = relationship("Student", back_populates="user", uselist=False)
    supervisor: Mapped["Supervisor"] = relationship("Supervisor", back_populates="user", uselist=False)

from app.models.student import Student
from app.models.supervisor import Supervisor