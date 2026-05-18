from decimal import Decimal
from pydantic import BaseModel

from app.schemas.user import UserRead

class StudentBase(BaseModel):
    album_number: str
    average_grade: Decimal

class StudentCreate(StudentBase):
    user_id: int

class StudentUpdate(BaseModel):
    average_grade: Decimal | None = None
    team_id: int | None = None

class StudentRead(StudentBase):
    id: int
    user_id: int
    team_id: int | None = None

    model_config = {
        "from_attributes": True
    }

class StudentWithUser(StudentRead):
    user: UserRead