from pydantic import BaseModel
from app.schemas.user import UserRead

class SupervisorBase(BaseModel):
    title: str | None = None
    capacity: int = 5
    description: str | None = None

class SupervisorCreate(SupervisorBase):
    user_id: int

class SupervisorUpdate(BaseModel):
    title: str | None = None
    capacity: int | None = None
    description: str | None = None

class SupervisorRead(SupervisorBase):
    id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }

class SupervisorWithUser(SupervisorRead):
    user: UserRead