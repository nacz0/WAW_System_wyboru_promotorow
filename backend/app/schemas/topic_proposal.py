from pydantic import BaseModel

class TopicProposalBase(BaseModel):
    title: str
    description: str | None = None
    is_active: bool = True

class TopicProposalCreate(TopicProposalBase):
    pass

class TopicProposalUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_active: bool | None = None

class TopicProposalRead(TopicProposalBase):
    id: int
    supervisor_id: int

    model_config = {
        "from_attributes": True
    }