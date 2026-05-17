from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Preference, RoundStatus, SelectionRound, Student, Supervisor, Team, TeamMember, TopicProposal, User, UserRole
from app.schemas import AssignmentRunResult
from app.services import hash_password, run_assignment


router = APIRouter()


def _get_or_create_user(db: Session, email: str, first_name: str, last_name: str, role: UserRole) -> User:
    user = db.execute(select(User).where(User.email == email)).scalars().first()
    if user is not None:
        return user
    user = User(
        email=email,
        password_hash=hash_password("demo1234"),
        first_name=first_name,
        last_name=last_name,
        role=role,
        is_active=True,
    )
    db.add(user)
    db.flush()
    return user


def _get_or_create_student(db: Session, user: User, album_number: str, average_grade: float) -> Student:
    student = db.execute(select(Student).where(Student.album_number == album_number)).scalars().first()
    if student is not None:
        return student
    student = Student(user=user, album_number=album_number, average_grade=average_grade)
    db.add(student)
    db.flush()
    return student


def _get_or_create_supervisor(db: Session, user: User, capacity: int, description: str) -> Supervisor:
    supervisor = db.execute(select(Supervisor).where(Supervisor.user_id == user.id)).scalars().first()
    if supervisor is not None:
        supervisor.capacity = capacity
        supervisor.description = description
        return supervisor
    supervisor = Supervisor(user=user, capacity=capacity, description=description)
    db.add(supervisor)
    db.flush()
    return supervisor


def _get_or_create_topic(db: Session, supervisor: Supervisor, title: str, description: str) -> TopicProposal:
    topic = (
        db.execute(
            select(TopicProposal).where(
                TopicProposal.supervisor_id == supervisor.id,
                TopicProposal.title == title,
            )
        )
        .scalars()
        .first()
    )
    if topic is not None:
        return topic
    topic = TopicProposal(supervisor=supervisor, title=title, description=description, is_active=True)
    db.add(topic)
    db.flush()
    return topic


def _get_or_create_team(db: Session, name: str, members: list[Student]) -> Team:
    team = db.execute(select(Team).where(Team.name == name)).scalars().first()
    if team is None:
        team = Team(name=name)
        db.add(team)
        db.flush()
    existing_member_ids = {member.student_id for member in team.members}
    for student in members:
        if student.id not in existing_member_ids:
            db.add(TeamMember(team=team, student=student))
    leader = sorted(members, key=lambda student: (-student.average_grade, student.album_number, student.id))[0]
    team.leader_student_id = leader.id
    db.flush()
    return team


def _get_or_create_round(db: Session) -> SelectionRound:
    selection_round = db.execute(select(SelectionRound).where(SelectionRound.name == "Demo 2026")).scalars().first()
    if selection_round is not None:
        selection_round.status = RoundStatus.open
        return selection_round
    now = datetime.now(timezone.utc)
    selection_round = SelectionRound(
        name="Demo 2026",
        starts_at=now - timedelta(days=1),
        ends_at=now + timedelta(days=7),
        status=RoundStatus.open,
    )
    db.add(selection_round)
    db.flush()
    return selection_round


def _get_or_create_preference(
    db: Session,
    selection_round: SelectionRound,
    supervisor: Supervisor,
    priority: int,
    student: Student | None = None,
    team: Team | None = None,
) -> Preference:
    query = select(Preference).where(
        Preference.selection_round_id == selection_round.id,
        Preference.priority == priority,
    )
    if student is not None:
        query = query.where(Preference.student_id == student.id)
    else:
        query = query.where(Preference.team_id == team.id)
    preference = db.execute(query).scalars().first()
    if preference is not None:
        preference.supervisor_id = supervisor.id
        return preference
    preference = Preference(
        selection_round=selection_round,
        student=student,
        team=team,
        priority=priority,
        supervisor=supervisor,
    )
    db.add(preference)
    db.flush()
    return preference


@router.post("/seed", response_model=AssignmentRunResult)
def seed_demo_data(db: Session = Depends(get_db)) -> AssignmentRunResult:
    _get_or_create_user(db, "admin@waw.edu.pl", "Admin", "Systemu", UserRole.admin)

    kowalski_user = _get_or_create_user(db, "jan.kowalski@waw.edu.pl", "Jan", "Kowalski", UserRole.supervisor)
    nowak_user = _get_or_create_user(db, "marta.nowak@waw.edu.pl", "Marta", "Nowak", UserRole.supervisor)
    wisniewska_user = _get_or_create_user(db, "olga.wisniewska@waw.edu.pl", "Olga", "Wisniewska", UserRole.supervisor)

    kowalski = _get_or_create_supervisor(db, kowalski_user, 2, "Systemy informacyjne i aplikacje webowe")
    nowak = _get_or_create_supervisor(db, nowak_user, 1, "Analiza danych i uczenie maszynowe")
    wisniewska = _get_or_create_supervisor(db, wisniewska_user, 2, "Bazy danych i hurtownie danych")

    _get_or_create_topic(db, kowalski, "System rezerwacji zasobow", "Aplikacja webowa z panelem administratora")
    _get_or_create_topic(db, nowak, "Predykcja wynikow studentow", "Model analityczny oparty o dane historyczne")
    _get_or_create_topic(db, wisniewska, "Projekt hurtowni danych", "Model relacyjny i raportowanie")

    anna = _get_or_create_student(
        db,
        _get_or_create_user(db, "anna.zielinska@student.waw.edu.pl", "Anna", "Zielinska", UserRole.student),
        "100001",
        4.80,
    )
    bartek = _get_or_create_student(
        db,
        _get_or_create_user(db, "bartek.kaczmarek@student.waw.edu.pl", "Bartek", "Kaczmarek", UserRole.student),
        "100002",
        4.55,
    )
    celina = _get_or_create_student(
        db,
        _get_or_create_user(db, "celina.wojcik@student.waw.edu.pl", "Celina", "Wojcik", UserRole.student),
        "100003",
        4.90,
    )
    daniel = _get_or_create_student(
        db,
        _get_or_create_user(db, "daniel.mazur@student.waw.edu.pl", "Daniel", "Mazur", UserRole.student),
        "100004",
        4.20,
    )
    ewa = _get_or_create_student(
        db,
        _get_or_create_user(db, "ewa.lis@student.waw.edu.pl", "Ewa", "Lis", UserRole.student),
        "100005",
        4.00,
    )

    team = _get_or_create_team(db, "Zespol AI", [bartek, ewa])
    selection_round = _get_or_create_round(db)

    _get_or_create_preference(db, selection_round, kowalski, 1, student=celina)
    _get_or_create_preference(db, selection_round, nowak, 1, student=anna)
    _get_or_create_preference(db, selection_round, kowalski, 2, student=anna)
    _get_or_create_preference(db, selection_round, kowalski, 1, team=team)
    _get_or_create_preference(db, selection_round, wisniewska, 2, team=team)
    _get_or_create_preference(db, selection_round, nowak, 1, student=daniel)
    _get_or_create_preference(db, selection_round, wisniewska, 2, student=daniel)

    db.commit()
    assignments, unassigned = run_assignment(db, selection_round.id)
    return AssignmentRunResult(selection_round_id=selection_round.id, assignments=assignments, unassigned=unassigned)
