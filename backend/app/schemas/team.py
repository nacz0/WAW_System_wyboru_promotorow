from pydantic import BaseModel
from app.schemas.student import StudentRead

class TeamBase(BaseModel):
    name: str
    max_size: int = 5

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: str | None = None
    max_size: int | None = None

class TeamRead(TeamBase):
    id: int
    leader_student_id: int | None = None
    assigned_supervisor_id: int | None = None

    model_config = {
        "from_attributes": True
    }

class TeamWithMembers(TeamRead):
    members: list[StudentRead] = []