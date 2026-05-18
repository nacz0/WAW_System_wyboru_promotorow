from datetime import datetime
from pydantic import BaseModel

class AssignmentBase(BaseModel):
    id: int
    selection_round_id: int
    student_id: int | None = None
    team_id: int | None = None
    supervisor_id: int
    assigned_at: datetime
    assignment_source: str

    model_config = {
        "from_attributes": True
    }

class AssignmentRead(AssignmentBase):
    pass