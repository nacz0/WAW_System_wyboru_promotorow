from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.db.session import get_db
from app.models import Supervisor, TopicProposal, User, UserRole
from app.schemas import SupervisorCreate, SupervisorRead, SupervisorUpdate, TopicProposalCreate, TopicProposalRead


router = APIRouter()


@router.post("", response_model=SupervisorRead, status_code=status.HTTP_201_CREATED)
def create_supervisor(
    payload: SupervisorCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.admin)),
) -> Supervisor:
    user = db.get(User, payload.user_id)
    if user is None or user.role != UserRole.supervisor:
        raise HTTPException(status_code=400, detail="supervisor must reference an existing supervisor user")

    supervisor = Supervisor(
        user_id=payload.user_id,
        capacity=payload.capacity,
        description=payload.description,
    )
    db.add(supervisor)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="supervisor for this user already exists") from exc
    db.refresh(supervisor)
    return supervisor


@router.get("", response_model=list[SupervisorRead])
def list_supervisors(
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[Supervisor]:
    return list(db.execute(select(Supervisor).order_by(Supervisor.id)).scalars().all())


@router.get("/{supervisor_id}", response_model=SupervisorRead)
def get_supervisor(
    supervisor_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> Supervisor:
    supervisor = db.get(Supervisor, supervisor_id)
    if supervisor is None:
        raise HTTPException(status_code=404, detail="supervisor not found")
    return supervisor


@router.patch("/{supervisor_id}", response_model=SupervisorRead)
def update_supervisor(
    supervisor_id: int,
    payload: SupervisorUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.admin)),
) -> Supervisor:
    supervisor = db.get(Supervisor, supervisor_id)
    if supervisor is None:
        raise HTTPException(status_code=404, detail="supervisor not found")
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(supervisor, field, value)
    db.commit()
    db.refresh(supervisor)
    return supervisor


@router.post("/{supervisor_id}/topics", response_model=TopicProposalRead, status_code=status.HTTP_201_CREATED)
def create_topic(
    supervisor_id: int,
    payload: TopicProposalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TopicProposal:
    supervisor = db.get(Supervisor, supervisor_id)
    if supervisor is None:
        raise HTTPException(status_code=404, detail="supervisor not found")
    if current_user.role != UserRole.admin and (
        current_user.supervisor is None or current_user.supervisor.id != supervisor_id
    ):
        raise HTTPException(status_code=403, detail="insufficient permissions")
    topic = TopicProposal(supervisor_id=supervisor_id, **payload.model_dump())
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


@router.get("/{supervisor_id}/topics", response_model=list[TopicProposalRead])
def list_topics(
    supervisor_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[TopicProposal]:
    if db.get(Supervisor, supervisor_id) is None:
        raise HTTPException(status_code=404, detail="supervisor not found")
    return list(
        db.execute(
            select(TopicProposal).where(TopicProposal.supervisor_id == supervisor_id).order_by(TopicProposal.id)
        )
        .scalars()
        .all()
    )
