from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.db.session import get_db
from app.models import Assignment, User, UserRole
from app.schemas import AssignmentRead, AssignmentRunResult
from app.services import run_assignment


router = APIRouter()


@router.post("/run/{selection_round_id}", response_model=AssignmentRunResult)
def run_selection_round_assignment(
    selection_round_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.admin)),
) -> AssignmentRunResult:
    try:
        assignments, unassigned = run_assignment(db, selection_round_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return AssignmentRunResult(selection_round_id=selection_round_id, assignments=assignments, unassigned=unassigned)


@router.get("", response_model=list[AssignmentRead])
def list_assignments(
    selection_round_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[Assignment]:
    query = select(Assignment).order_by(Assignment.selection_round_id, Assignment.id)
    if selection_round_id is not None:
        query = query.where(Assignment.selection_round_id == selection_round_id)
    return list(db.execute(query).scalars().all())
