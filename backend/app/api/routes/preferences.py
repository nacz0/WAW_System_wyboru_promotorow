from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import Preference, RoundStatus, SelectionRound, Student, Supervisor, Team, User, UserRole
from app.schemas import PreferenceCreate, PreferenceRead


router = APIRouter()


def _actor_filter(query, payload: PreferenceCreate):
    if payload.student_id is not None:
        return query.where(Preference.student_id == payload.student_id)
    return query.where(Preference.team_id == payload.team_id)


def _ensure_preference_owner(payload: PreferenceCreate, current_user: User, db: Session) -> None:
    if current_user.role == UserRole.admin:
        return
    if current_user.role != UserRole.student or current_user.student is None:
        raise HTTPException(status_code=403, detail="only students or admins can submit preferences")
    if payload.student_id is not None:
        if payload.student_id != current_user.student.id:
            raise HTTPException(status_code=403, detail="cannot submit preferences for another student")
        return
    team = db.get(Team, payload.team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="team not found")
    if team.leader_student_id != current_user.student.id:
        raise HTTPException(status_code=403, detail="only team leader can submit team preferences")


@router.post("", response_model=PreferenceRead, status_code=status.HTTP_201_CREATED)
def create_preference(
    payload: PreferenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Preference:
    _ensure_preference_owner(payload, current_user, db)
    selection_round = db.get(SelectionRound, payload.selection_round_id)
    if selection_round is None:
        raise HTTPException(status_code=404, detail="selection round not found")
    if selection_round.status in {RoundStatus.closed, RoundStatus.assigned}:
        raise HTTPException(status_code=400, detail="selection round no longer accepts preferences")
    if db.get(Supervisor, payload.supervisor_id) is None:
        raise HTTPException(status_code=404, detail="supervisor not found")
    if payload.student_id is not None and db.get(Student, payload.student_id) is None:
        raise HTTPException(status_code=404, detail="student not found")
    if payload.team_id is not None and db.get(Team, payload.team_id) is None:
        raise HTTPException(status_code=404, detail="team not found")

    duplicate_supervisor_query = select(Preference).where(
        Preference.selection_round_id == payload.selection_round_id,
        Preference.supervisor_id == payload.supervisor_id,
    )
    duplicate_supervisor_query = _actor_filter(duplicate_supervisor_query, payload)
    if db.execute(duplicate_supervisor_query).scalars().first() is not None:
        raise HTTPException(status_code=409, detail="this supervisor is already selected by this actor")

    preference = Preference(**payload.model_dump())
    db.add(preference)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="preference priority is already used by this actor") from exc
    db.refresh(preference)
    return preference


@router.get("", response_model=list[PreferenceRead])
def list_preferences(
    selection_round_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Preference]:
    query = select(Preference).order_by(Preference.selection_round_id, Preference.priority, Preference.id)
    if selection_round_id is not None:
        query = query.where(Preference.selection_round_id == selection_round_id)
    if current_user.role == UserRole.student:
        if current_user.student is None:
            return []
        team_ids = [membership.team_id for membership in current_user.student.team_memberships]
        query = query.where(
            (Preference.student_id == current_user.student.id) | (Preference.team_id.in_(team_ids))
        )
    elif current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="insufficient permissions")
    return list(db.execute(query).scalars().all())
