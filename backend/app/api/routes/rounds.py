from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.db.session import get_db
from app.models import SelectionRound, User, UserRole
from app.schemas import SelectionRoundCreate, SelectionRoundRead, SelectionRoundStatusUpdate


router = APIRouter()


@router.post("", response_model=SelectionRoundRead, status_code=status.HTTP_201_CREATED)
def create_round(
    payload: SelectionRoundCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.admin)),
) -> SelectionRound:
    selection_round = SelectionRound(**payload.model_dump())
    db.add(selection_round)
    db.commit()
    db.refresh(selection_round)
    return selection_round


@router.get("", response_model=list[SelectionRoundRead])
def list_rounds(
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[SelectionRound]:
    return list(db.execute(select(SelectionRound).order_by(SelectionRound.starts_at.desc())).scalars().all())


@router.get("/{selection_round_id}", response_model=SelectionRoundRead)
def get_round(
    selection_round_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> SelectionRound:
    selection_round = db.get(SelectionRound, selection_round_id)
    if selection_round is None:
        raise HTTPException(status_code=404, detail="selection round not found")
    return selection_round


@router.patch("/{selection_round_id}/status", response_model=SelectionRoundRead)
def update_round_status(
    selection_round_id: int,
    payload: SelectionRoundStatusUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.admin)),
) -> SelectionRound:
    selection_round = db.get(SelectionRound, selection_round_id)
    if selection_round is None:
        raise HTTPException(status_code=404, detail="selection round not found")
    selection_round.status = payload.status
    db.commit()
    db.refresh(selection_round)
    return selection_round
