from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user, require_admin
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.team import Team
from app.models.preference import Preference
from app.models.selection_round import SelectionRound, RoundStatus
from app.schemas.preference import PreferenceRead, PreferenceBulkCreate


router = APIRouter(prefix="/preferences", tags=["preferences"])

@router.get("/round/{round_id}", response_model=list[PreferenceRead])
def list_preferences(
    round_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all preferences for a given selection round. Admins see all, supervisors see only their students' preferences."""
    query = db.query(Preference).filter(Preference.selection_round_id == round_id)

    if current_user.role == UserRole.STUDENT:
        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            return []
        if student.team_id:
            query = query.filter(Preference.team_id == student.team_id)
        else:
            query = query.filter(Preference.student_id == student.id)

    elif current_user.role == UserRole.SUPERVISOR:
        sup = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not sup:
            return []
        query = query.filter(Preference.supervisor_id == sup.id)

    return query.order_by(Preference.priority).all()

@router.get("/my/{round_id}", response_model=list[PreferenceRead])
def get_my_preferences(
    round_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the current user's preferences for a given selection round."""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can access their preferences")
    
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")  
    
    query = db.query(Preference).filter(Preference.selection_round_id == round_id)
    if student.team_id:
        query = query.filter(Preference.team_id == student.team_id)
    else:
        query = query.filter(Preference.student_id == student.id)

    return query.order_by(Preference.priority).all()

@router.post("/round/{round_id}", response_model=list[PreferenceRead], status_code=status.HTTP_201_CREATED)
def create_preferences(
    round_id: int,
    data: PreferenceBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit preferences for a given selection round. Replaces existing preferences."""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can create preferences")


    selection_round = db.get(SelectionRound, round_id)
    if not selection_round:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Selection round not found")
    if selection_round.status != RoundStatus.OPEN:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Selection round is not open for preferences")

    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")

    is_team = student.team_id is not None

    #Delete existing preferences for this student/team and round
    if is_team:
        db.query(Preference).filter(Preference.selection_round_id == round_id, Preference.team_id == student.team_id).delete()
    else:
        db.query(Preference).filter(Preference.selection_round_id == round_id, Preference.student_id == student.id).delete()

    created = []
    for pref_data in data.preferences:
        pref = Preference(
            selection_round_id=round_id,
            student_id=student.id if not is_team else None,
            team_id=student.team_id if is_team else None,
            priority=pref_data.priority,
            supervisor_id=pref_data.supervisor_id,
        )
        db.add(pref)
        created.append(pref)

    db.commit()
    for p in created:
        db.refresh(p)
    return created

@router.delete("/round/{round_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_preferences(
    round_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete the current user's preferences for a given selection round."""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can delete their preferences")
    
    selection_round = db.get(SelectionRound, round_id)
    if not selection_round or selection_round.status != RoundStatus.OPEN:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Selection round not found or not open")
    
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")  
    
    if student.team_id:
        db.query(Preference).filter(Preference.selection_round_id == round_id, Preference.team_id == student.team_id).delete()
    else:
        db.query(Preference).filter(Preference.selection_round_id == round_id, Preference.student_id == student.id).delete()

    db.commit()