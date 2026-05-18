from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user, require_admin
from app.models.user import User, UserRole
from app.models.selection_round import SelectionRound
from app.models.assignment import Assignment
from app.models.student import Student
from app.models.supervisor import Supervisor
from app.schemas.assignment import AssignmentRead
from app.services.allocation_service import run_allocation

router = APIRouter(prefix="/assignments", tags=["assignments"])

@router.get("/round/{round_id}", response_model=list[AssignmentRead])
def list_assignments(
    round_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all assignments for a given selection round. Admins see all, supervisors see only their students."""
    query = db.query(Assignment).filter(Assignment.round_id == round_id)

    if current_user.role == UserRole.STUDENT:
        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            return []
        if student.team_id:
            query = query.filter(Assignment.team_id == student.team_id)
        else:
            query = query.filter(Assignment.student_id == student.id)

    elif current_user.role == UserRole.SUPERVISOR:
        sup = db.query(Supervisor).filter(Supervisor.user_id == current_user.id).first()
        if not sup:
            return []
        query = query.filter(Assignment.supervisor_id == sup.id)

    return query.all()

@router.post("/round/{round_id}/run")
def run_allocation_endpoint(
    round_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """Run allocation for a given selection round. Only admins can perform this action."""
    result = run_allocation(db, round_id)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    return result