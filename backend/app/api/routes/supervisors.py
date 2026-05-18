from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.core.dependencies import get_current_user, require_admin, require_admin_or_supervisor
from app.models.user import User, UserRole
from app.models.supervisor import Supervisor
from app.schemas.supervisor import SupervisorRead, SupervisorWithUser, SupervisorUpdate
from app.services.import_service import import_supervisors_from_csv

router = APIRouter(prefix="/supervisors", tags=["supervisors"])

@router.get("/", response_model=list[SupervisorWithUser])
def list_supervisors(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Supervisor)
        .options(joinedload(Supervisor.user))
        .order_by(Supervisor.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

@router.get("/me", response_model=SupervisorWithUser)
def get_my_supervisor_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.SUPERVISOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only supervisors can access this endpoint")
    supervisor = db.query(Supervisor).options(joinedload(Supervisor.user)).filter(Supervisor.user_id == current_user.id).first()
    if not supervisor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supervisor profile not found")
    return supervisor

@router.get("/{supervisor_id}", response_model=SupervisorWithUser)
def get_supervisor(
    supervisor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    supervisor = db.query(Supervisor).options(joinedload(Supervisor.user)).filter(Supervisor.id == supervisor_id).first()
    if not supervisor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supervisor not found")
    return supervisor

@router.patch("/{supervisor_id}", response_model=SupervisorRead)
def update_supervisor(
    supervisor_id: int,
    data: SupervisorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_supervisor)
):
    supervisor = db.get(Supervisor, supervisor_id)
    if not supervisor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supervisor not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(supervisor, key, value)
    db.commit()
    db.refresh(supervisor)
    return supervisor

@router.post("/import", status_code=status.HTTP_201_CREATED)
def import_supervisors(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type. Please upload a CSV file.")

    
    content = file.file.read()
    result = import_supervisors_from_csv(db, content)
    return result