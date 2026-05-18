from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user, require_admin
from app.models.user import User
from app.models.selection_round import SelectionRound, RoundStatus
from app.schemas.selection_round import SelectionRoundCreate, SelectionRoundUpdate, SelectionRoundRead

router = APIRouter(prefix="/rounds", tags=["selection-rounds"])

@router.get("/", response_model=list[SelectionRoundRead])
def list_rounds(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return db.query(SelectionRound).order_by(SelectionRound.created_at.desc()).offset(skip).limit(limit).all()

@router.post("/", response_model=SelectionRoundRead, status_code=status.HTTP_201_CREATED)
def create_round(
    data: SelectionRoundCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    sr = db.get(**data.model_dump(), status=RoundStatus.DRAFT)
    db.add(sr)
    db.commit()
    db.refresh(sr)
    return sr

@router.get("/{round_id}", response_model=SelectionRoundRead)
def get_round(
    round_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sr = db.get(SelectionRound, round_id)
    if not sr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Selection round not found")
    return sr

@router.patch("/{round_id}", response_model=SelectionRoundRead)
def update_round(
    round_id: int,
    data: SelectionRoundUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    sr = db.get(SelectionRound, round_id)
    if not sr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Selection round not found")
    update_data = data.model_dump(exclude_unset=True)

    if "status" in update_data:
        new_status = update_data["status"]
        valid_transitions = {
            RoundStatus.DRAFT: [RoundStatus.OPEN],
            RoundStatus.OPEN: [RoundStatus.CLOSED],
            RoundStatus.CLOSED: [RoundStatus.OPEN, RoundStatus.COMPLETED],
            RoundStatus.COMPLETED: [],
        }
        if new_status not in valid_transitions.get(sr.status, []):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot change status from {sr.status.value} to {new_status.value}")
        
    for field, value in update_data.items():
        setattr(sr, field, value)

    db.commit()
    db.refresh(sr)
    return sr

@router.delete("/{round_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_round(
    round_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    sr = db.get(SelectionRound, round_id)
    if not sr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Selection round not found")
    if sr.status == RoundStatus.COMPLETED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only rounds in DRAFT status can be deleted")
    db.delete(sr)
    db.commit()
