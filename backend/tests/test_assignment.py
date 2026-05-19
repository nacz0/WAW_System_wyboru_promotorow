from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models import Preference, RoundStatus, SelectionRound, Student, Supervisor, Team, TeamMember, User, UserRole
from app.services.assignment import run_assignment


@pytest.fixture()
def db() -> Session:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def make_user(db: Session, email: str, role: UserRole, first_name: str = "Test", last_name: str = "User") -> User:
    user = User(
        email=email,
        password_hash="hash",
        first_name=first_name,
        last_name=last_name,
        role=role,
    )
    db.add(user)
    db.flush()
    return user


def make_student(db: Session, album_number: str, average_grade: float) -> Student:
    user = make_user(
        db,
        f"student-{album_number}@example.test",
        UserRole.student,
        first_name=f"Student{album_number}",
    )
    student = Student(user=user, album_number=album_number, average_grade=average_grade)
    db.add(student)
    db.flush()
    return student


def make_supervisor(db: Session, email: str, capacity: int) -> Supervisor:
    user = make_user(db, email, UserRole.supervisor, first_name=email.split("@")[0])
    supervisor = Supervisor(user=user, capacity=capacity)
    db.add(supervisor)
    db.flush()
    return supervisor


def make_round(db: Session) -> SelectionRound:
    now = datetime.now(timezone.utc)
    selection_round = SelectionRound(
        name="Test round",
        starts_at=now - timedelta(days=1),
        ends_at=now + timedelta(days=1),
        status=RoundStatus.open,
    )
    db.add(selection_round)
    db.flush()
    return selection_round


def add_preference(
    db: Session,
    selection_round: SelectionRound,
    supervisor: Supervisor,
    priority: int,
    student: Student | None = None,
    team: Team | None = None,
) -> Preference:
    preference = Preference(
        selection_round=selection_round,
        student=student,
        team=team,
        supervisor=supervisor,
        priority=priority,
    )
    db.add(preference)
    db.flush()
    return preference


def make_team(db: Session, name: str, students: list[Student]) -> Team:
    team = Team(name=name)
    db.add(team)
    db.flush()
    for student in students:
        db.add(TeamMember(team=team, student=student))
    leader = sorted(students, key=lambda item: (-item.average_grade, item.album_number, item.id))[0]
    team.leader_student_id = leader.id
    db.flush()
    return team


def test_higher_average_gets_first_choice(db: Session) -> None:
    first_supervisor = make_supervisor(db, "first@example.test", capacity=1)
    second_supervisor = make_supervisor(db, "second@example.test", capacity=1)
    high_average = make_student(db, "100001", 4.9)
    low_average = make_student(db, "100002", 4.1)
    selection_round = make_round(db)

    add_preference(db, selection_round, first_supervisor, 1, student=low_average)
    add_preference(db, selection_round, second_supervisor, 2, student=low_average)
    add_preference(db, selection_round, first_supervisor, 1, student=high_average)
    add_preference(db, selection_round, second_supervisor, 2, student=high_average)

    assignments, unassigned = run_assignment(db, selection_round.id)

    by_student = {assignment.student_id: assignment.supervisor_id for assignment in assignments}
    assert by_student[high_average.id] == first_supervisor.id
    assert by_student[low_average.id] == second_supervisor.id
    assert unassigned == []


def test_no_capacity_returns_unassigned_candidate(db: Session) -> None:
    supervisor = make_supervisor(db, "supervisor@example.test", capacity=1)
    high_average = make_student(db, "100001", 4.9)
    low_average = make_student(db, "100002", 4.1)
    selection_round = make_round(db)

    add_preference(db, selection_round, supervisor, 1, student=high_average)
    add_preference(db, selection_round, supervisor, 1, student=low_average)

    assignments, unassigned = run_assignment(db, selection_round.id)

    assert len(assignments) == 1
    assert assignments[0].student_id == high_average.id
    assert unassigned == [
        {
            "actor_type": "student",
            "actor_id": low_average.id,
            "reason": "no_supervisor_capacity_for_preferences",
        }
    ]


def test_team_uses_multiple_places_and_leader_average(db: Session) -> None:
    small_supervisor = make_supervisor(db, "small@example.test", capacity=1)
    large_supervisor = make_supervisor(db, "large@example.test", capacity=2)
    student_a = make_student(db, "100001", 4.2)
    student_b = make_student(db, "100002", 4.8)
    team = make_team(db, "Team A", [student_a, student_b])
    selection_round = make_round(db)

    add_preference(db, selection_round, small_supervisor, 1, team=team)
    add_preference(db, selection_round, large_supervisor, 2, team=team)

    assignments, unassigned = run_assignment(db, selection_round.id)

    assert len(assignments) == 1
    assert assignments[0].team_id == team.id
    assert assignments[0].supervisor_id == large_supervisor.id
    assert assignments[0].assignment_source == "preference_2"
    assert team.leader_student_id == student_b.id
    assert unassigned == []


def test_assignment_is_repeatable_and_does_not_duplicate_results(db: Session) -> None:
    supervisor = make_supervisor(db, "supervisor@example.test", capacity=2)
    first_student = make_student(db, "100001", 4.9)
    second_student = make_student(db, "100002", 4.1)
    selection_round = make_round(db)

    add_preference(db, selection_round, supervisor, 1, student=first_student)
    add_preference(db, selection_round, supervisor, 1, student=second_student)

    first_run, first_unassigned = run_assignment(db, selection_round.id)
    second_run, second_unassigned = run_assignment(db, selection_round.id)

    assert [(item.student_id, item.supervisor_id) for item in first_run] == [
        (first_student.id, supervisor.id),
        (second_student.id, supervisor.id),
    ]
    assert [(item.student_id, item.supervisor_id) for item in second_run] == [
        (first_student.id, supervisor.id),
        (second_student.id, supervisor.id),
    ]
    assert first_unassigned == []
    assert second_unassigned == []
    assert len(second_run) == 2
