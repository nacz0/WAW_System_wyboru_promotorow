from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import require_admin_or_supervisor, get_current_user
from app.models.user import User, UserRole
from app.models.supervisor import Supervisor
from app.models.topic_proposal import TopicProposal
from app.schemas.topic_proposal import TopicProposalCreate, TopicProposalRead, TopicProposalUpdate

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("/", response_model=list[TopicProposalRead])
def list_topics(
    supervisor_id: int | None = None,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(TopicProposal)
    if supervisor_id:
        query = query.filter(TopicProposal.supervisor_id == supervisor_id)
    if active_only:
        query = query.filter(TopicProposal.is_active == True)
    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=TopicProposalRead, status_code=status.HTTP_201_CREATED)
def create_topic(
    data: TopicProposalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_supervisor),
):
    if current_user.role == UserRole.SUPERVISOR:
        sup = db.query(Supervisor).filter(Supervisor.user_id == current_user.id).first()
        if not sup:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supervisor profile not found")
        supervisor_id = sup.id
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin must use POST /topics/{supervisor_id} endpoint",
        )
    topic = TopicProposal(supervisor_id=supervisor_id, **data.model_dump())
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic

@router.post("/{supervisor_id}", response_model=TopicProposalRead, status_code=status.HTTP_201_CREATED)
def create_topic_for_supervisor(
    supervisor_id: int,
    data: TopicProposalCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin_or_supervisor)
):
    sup = db.get(Supervisor, supervisor_id)
    if not sup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supervisor not found")
    if _admin.role == UserRole.SUPERVISOR and sup.user_id != _admin.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot create topics for another supervisor")
    topic = TopicProposal(supervisor_id=supervisor_id, **data.model_dump())
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


@router.post("/{topic_id}", response_model=TopicProposalRead)
def update_topic(
    topic_id: int,
    data: TopicProposalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_supervisor),
):
    topic = db.get(TopicProposal, topic_id)
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic proposal not found")

    if current_user.role == UserRole.SUPERVISOR:
        sup = db.query(Supervisor).filter(Supervisor.user_id == current_user.id).first()
        if not sup or topic.supervisor_id != sup.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this topic proposal")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(topic, field, value)

    db.commit()
    db.refresh(topic)
    return topic

@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_supervisor),
):
    topic = db.get(TopicProposal, topic_id)
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    if current_user.role == UserRole.SUPERVISOR:
        sup = db.query(Supervisor).filter(Supervisor.user_id == current_user.id).first()
        if not sup or sup.id != topic.supervisor_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannto delete another supervisor's topic")
    db.delete(topic)
    db.commit()