from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models import RoundStatus, UserRole


class UserBase(BaseModel):
    email: str = Field(max_length=255)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    role: UserRole
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=255)


class UserRead(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StudentBase(BaseModel):
    user_id: int
    album_number: str = Field(min_length=1, max_length=32)
    average_grade: float = Field(ge=2.0, le=5.0)


class StudentCreate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: int
    user: UserRead | None = None

    model_config = ConfigDict(from_attributes=True)


class SupervisorBase(BaseModel):
    user_id: int
    capacity: int = Field(ge=0)
    description: str | None = None


class SupervisorCreate(SupervisorBase):
    pass


class SupervisorUpdate(BaseModel):
    capacity: int | None = Field(default=None, ge=0)
    description: str | None = None


class SupervisorRead(SupervisorBase):
    id: int
    user: UserRead | None = None

    model_config = ConfigDict(from_attributes=True)


class TopicProposalBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    is_active: bool = True


class TopicProposalCreate(TopicProposalBase):
    pass


class TopicProposalRead(TopicProposalBase):
    id: int
    supervisor_id: int

    model_config = ConfigDict(from_attributes=True)


class TeamBase(BaseModel):
    name: str = Field(min_length=1, max_length=150)


class TeamCreate(TeamBase):
    member_student_ids: list[int] = Field(default_factory=list)


class TeamMemberRead(BaseModel):
    id: int
    team_id: int
    student_id: int
    student: StudentRead | None = None

    model_config = ConfigDict(from_attributes=True)


class TeamRead(TeamBase):
    id: int
    leader_student_id: int | None = None
    assigned_supervisor_id: int | None = None
    members: list[TeamMemberRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class TeamMemberCreate(BaseModel):
    student_id: int


class SelectionRoundBase(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    starts_at: datetime
    ends_at: datetime
    status: RoundStatus = RoundStatus.draft

    @model_validator(mode="after")
    def validate_dates(self) -> "SelectionRoundBase":
        if self.ends_at <= self.starts_at:
            raise ValueError("ends_at must be later than starts_at")
        return self


class SelectionRoundCreate(SelectionRoundBase):
    pass


class SelectionRoundStatusUpdate(BaseModel):
    status: RoundStatus


class SelectionRoundRead(SelectionRoundBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PreferenceBase(BaseModel):
    selection_round_id: int
    student_id: int | None = None
    team_id: int | None = None
    priority: int = Field(ge=1, le=3)
    supervisor_id: int

    @model_validator(mode="after")
    def validate_owner(self) -> "PreferenceBase":
        if (self.student_id is None and self.team_id is None) or (
            self.student_id is not None and self.team_id is not None
        ):
            raise ValueError("preference must belong to exactly one student or team")
        return self


class PreferenceCreate(PreferenceBase):
    pass


class PreferenceRead(PreferenceBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssignmentRead(BaseModel):
    id: int
    selection_round_id: int
    student_id: int | None = None
    team_id: int | None = None
    supervisor_id: int
    assigned_at: datetime
    assignment_source: str

    model_config = ConfigDict(from_attributes=True)


class AssignmentRunResult(BaseModel):
    selection_round_id: int
    assignments: list[AssignmentRead]
    unassigned: list[dict[str, object]]
