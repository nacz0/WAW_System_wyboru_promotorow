import csv
import io
from decimal import Decimal, InvalidOperation
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.supervisor import Supervisor
from app.models.user import User, UserRole
from app.core.security import hash_password

def import_students_from_csv(db: Session, file_content: bytes) -> dict:
    """Import students from a CSV file. The CSV should have columns: email, first_name, last_name, album_number, average_grade, password."""

    text = file_content.decode('utf-8-sig')
    reader = csv.DictReader(io.StringIO(text), delimiter=';')

    created = 0
    skipped = 0
    errors = []

    for i, row in enumerate(reader, start=2):
        try:
            email = row.get('email', '').strip()
            first_name = row.get('first_name', '').strip()
            last_name = row.get('last_name', '').strip()
            album_number = row.get('album_number', '').strip()
            avg_grade_str = row.get('average_grade', '').strip()
            password = row.get('password', '').strip()

            if not all([email, first_name, last_name, album_number, avg_grade_str, password]):
                errors.append(f"Row {i}: Missing required fields")
                skipped += 1
                continue

            try:
                average_grade = Decimal(avg_grade_str)
            except InvalidOperation:
                errors.append(f"Row {i}: Invalid average_grade '{avg_grade_str}'")
                skipped += 1
                continue

            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                errors.append(f"Row {i}: User with email '{email}' already exists")
                skipped += 1
                continue

            existing_stduent = db.query(Student).filter(Student.album_number == album_number).first()
            if existing_stduent:
                errors.append(f"Row {i}: Student with album number '{album_number}' already exists")
                skipped += 1
                continue

            user = User(
                email=email,
                password_hash=hash_password(password),
                first_name=first_name,
                last_name=last_name,
                role=UserRole.STUDENT,
                is_active=True
            )
            db.add(user)
            db.flush()

            student = Student(
                user_id=user.id,
                album_number=album_number,
                average_grade=average_grade,
            )
            db.add(student)
            created += 1

        except Exception as e:
            errors.append(f"Row {i}: Unexpected error: {str(e)}")
            skipped += 1

    db.commit()
    return {
        "created": created,
        "skipped": skipped,
        "errors": errors
    }


def import_supervisors_from_csv(db: Session, file_content: bytes) -> dict:
    """Import supervisors from a CSV file. The CSV should have columns: email, first_name, last_name, title, capacity, description, password."""

    text = file_content.decode('utf-8-sig')
    reader = csv.DictReader(io.StringIO(text), delimiter=';')

    created = 0
    skipped = 0
    errors = []

    for i, row in enumerate(reader, start=2):
        try:
            email = row.get('email', '').strip()
            first_name = row.get('first_name', '').strip()
            last_name = row.get('last_name', '').strip()
            title = row.get('title', '').strip()
            capacity_str = row.get('capacity', '5').strip()
            description = row.get('description', '').strip()
            password = row.get('password', '').strip()

            if not all([email, first_name, last_name, password]):
                errors.append(f"Row {i}: Missing required fields")
                skipped += 1
                continue

            try:
                capacity = int(capacity_str)
            except ValueError:
                errors.append(f"Row {i}: Invalid capacity '{capacity_str}'")
                skipped += 1
                continue

            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                errors.append(f"Row {i}: User with email '{email}' already exists")
                skipped += 1
                continue

            user = User(
                email=email,
                password_hash=hash_password(password),
                first_name=first_name,
                last_name=last_name,
                role=UserRole.SUPERVISOR,
                is_active=True
            )
            db.add(user)
            db.flush()

            supervisor = Supervisor(
                user_id=user.id,
                title=title or None,
                capacity=capacity,
                description=description,
            )
            db.add(supervisor)
            created += 1

        except Exception as e:
            errors.append(f"Row {i}: Unexpected error: {str(e)}")
            skipped += 1

    db.commit()
    return {
        "created": created,
        "skipped": skipped,
        "errors": errors
    }