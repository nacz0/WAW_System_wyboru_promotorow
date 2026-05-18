from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.core.dependencies import get_current_user, require_admin
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.team import Team
from app.schemas.team import TeamRead, TeamCreate, TeamUpdate, TeamWithMembers

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/", response_model=list[TeamWithMembers])
def list_teams(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Team)
        .options(joinedload(Team.students).joinedload(Student.user))
        .order_by(Team.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

@router.post("/", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
def create_team(
    data: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.STUDENT]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins and students can create teams")
    
    team = Team(name=data.name, max_size=data.max_size)
    db.add(team)
    db.flush()  # Flush to get the team ID for the association

    if current_user.role == UserRole.STUDENT:
        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
        if student.team_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are already in a team")
        student.team_id = team.id
        team.leader_student_id = student.id

    db.commit()
    db.refresh(team)
    return team

@router.get("/{team_id}", response_model=TeamWithMembers)
def get_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    team = db.query(Team).options(joinedload(Team.students).joinedload(Student.user)).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team

@router.patch("/{team_id}", response_model=TeamRead)
def update_team(
    team_id: int,
    data: TeamUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(team, key, value)
    db.commit()
    db.refresh(team)
    return team

@router.post("/{team_id}/join", response_model=TeamRead)
def join_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Students joins an existing team."""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can join teams")
    
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    if student.team_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are already in a team")
    
    team = db.query(Team).options(joinedload(Team.students)).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
       
    if len(team.students) >= team.max_size:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team is already at maximum capacity")
    
    student.team_id = team.id
    db.commit()
    db.refresh(team)
    return team

@router.post("/{team_id}/leave", response_model=TeamRead)
def leave_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Students leaves their current team."""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can leave teams")
    
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    if student.team_id != team_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not a member of this team")
    
    team = db.query(Team).options(joinedload(Team.members)).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    
    student.team_id = None
    db.flush()
    
    remaining = db.query(Student).filter(Student.team_id == team_id).all()
    if not remaining:
        db.delete(team)
    else:
        _update_team_leader(db, team, members=remaining)

    
    db.commit()
    if remaining:
        db.refresh(team)
        return team
    return TeamRead(id=team_id, name="(Deleted)", max_size=0)

@router.post("/{team_id}/members/{student_id}", response_model=TeamRead)
def add_member_to_team(
    team_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    """Admin adds a student to an existing team."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    if student.team_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student is already in a team")
    team = db.query(Team).options(joinedload(Team.members)).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    
    
    if len(team.members) >= team.max_size:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team is already at maximum capacity")
    
    student.team_id = team.id
    _update_team_leader(db, team)  # In case the new member has a higher grade than the current leader
    db.commit()
    db.refresh(team)
    return team

@router.delete("/{team_id}/members/{student_id}", response_model=TeamRead)
def remove_member_from_team(
    team_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    """Admin removes a student from a team."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    if student.team_id != team_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student is not a member of this team")
    
    team = db.query(Team).options(joinedload(Team.members)).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    
    student.team_id = None
    db.flush()
    
    remaining = db.query(Student).filter(Student.team_id == team_id).all()
    if remaining:
        _update_team_leader(db, team, members=remaining)
    else:
        team.leader_student_id = None
    
    db.commit()
    db.refresh(team)
    return team

@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(
    team_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    
    for member in team.members:
        member.team_id = None
    team.leader_student_id = None
    db.flush()
    db.delete(team)
    db.commit()

def _update_team_leader(db: Session, team: Team, members: list[Student] | None = None):
    if members is None:
        members = db.query(Student).filter(Student.team_id == team.id).all()
    if members:
        leader = max(members, key=lambda s: (s.average_grade, -s.album_number))
        team.leader_student_id = leader.id
    else:
        team.leader_student_id = None