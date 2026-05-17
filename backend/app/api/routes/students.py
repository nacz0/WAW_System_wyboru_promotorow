from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.db.session import get_db
from app.models import Student, User, UserRole
from app.schemas import StudentCreate, StudentRead


router = APIRouter()


@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(
    payload: StudentCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.admin)),
) -> Student:
    user = db.get(User, payload.user_id)
    if user is None or user.role != UserRole.student:
        raise HTTPException(status_code=400, detail="student must reference an existing student user")

    student = Student(
        user_id=payload.user_id,
        album_number=payload.album_number,
        average_grade=payload.average_grade,
    )
    db.add(student)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="student user or album number already exists") from exc
    db.refresh(student)
    return student


@router.get("", response_model=list[StudentRead])
def list_students(
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[Student]:
    return list(db.execute(select(Student).order_by(Student.album_number)).scalars().all())


@router.get("/{student_id}", response_model=StudentRead)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Student:
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")
    if current_user.role != UserRole.admin and (current_user.student is None or current_user.student.id != student_id):
        raise HTTPException(status_code=403, detail="insufficient permissions")
    return student
