from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.db.session import get_db
from app.models import Student, Team, TeamMember, User, UserRole
from app.schemas import TeamCreate, TeamMemberCreate, TeamRead


router = APIRouter()


def _select_leader(team: Team) -> None:
    students = [membership.student for membership in team.members if membership.student is not None]
    if not students:
        team.leader_student_id = None
        return
    leader = sorted(students, key=lambda student: (-student.average_grade, student.album_number, student.id))[0]
    team.leader_student_id = leader.id


@router.post("", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
def create_team(
    payload: TeamCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.admin)),
) -> Team:
    team = Team(name=payload.name)
    db.add(team)
    try:
        db.flush()
        for student_id in payload.member_student_ids:
            student = db.get(Student, student_id)
            if student is None:
                raise HTTPException(status_code=400, detail=f"student {student_id} not found")
            db.add(TeamMember(team=team, student=student))
        db.flush()
        db.refresh(team)
        _select_leader(team)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="team name or member already exists") from exc
    db.refresh(team)
    return team


@router.get("", response_model=list[TeamRead])
def list_teams(
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[Team]:
    return list(db.execute(select(Team).order_by(Team.id)).scalars().all())


@router.get("/{team_id}", response_model=TeamRead)
def get_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Team:
    team = db.get(Team, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="team not found")
    if current_user.role != UserRole.admin and current_user.role != UserRole.supervisor:
        member_ids = {membership.student_id for membership in team.members}
        if current_user.student is None or current_user.student.id not in member_ids:
            raise HTTPException(status_code=403, detail="insufficient permissions")
    return team


@router.post("/{team_id}/members", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
def add_team_member(
    team_id: int,
    payload: TeamMemberCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.admin)),
) -> Team:
    team = db.get(Team, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="team not found")
    student = db.get(Student, payload.student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")
    db.add(TeamMember(team=team, student=student))
    try:
        db.flush()
        db.refresh(team)
        _select_leader(team)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="student already belongs to a team") from exc
    db.refresh(team)
    return team
