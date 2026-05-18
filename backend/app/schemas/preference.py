from pydantic import BaseModel, field_validator

class PreferenceBase(BaseModel):
    priority: int
    supervisor_id: int

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: int) -> int:
        if not 1 <= v <= 3:
            raise ValueError("Priority must be between 1 and 3")
        return v
    
class PreferenceCreate(PreferenceBase):
    pass

class PreferenceRead(PreferenceBase):
    id: int
    selection_round_id: int
    student_id: int | None = None
    team_id: int | None = None

    model_config = {
        "from_attributes": True
    }

class PreferenceBulkCreate(BaseModel):
    """Submit all 3 preferences at once."""
    preferences: list[PreferenceCreate]

    @field_validator("preferences")
    @classmethod
    def validate_preferences(cls, v: list[PreferenceCreate]) -> list[PreferenceCreate]:
        if len(v) > 3:
            raise ValueError("Maximum of 3 preferences allowed")
        priorities = [p.priority for p in v]
        if len(priorities) != len(set(priorities)):
            raise ValueError("Priorities must be unique")
        supervisor_ids = [p.supervisor_id for p in v]
        if len(supervisor_ids) != len(set(supervisor_ids)):
            raise ValueError("Cannot select the same supervisor for multiple preferences")
        return v