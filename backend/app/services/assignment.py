from dataclasses import dataclass

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import Assignment, Preference, RoundStatus, SelectionRound, Student, Supervisor, Team, TeamMember


@dataclass
class Candidate:
    actor_type: str
    actor_id: int
    score: float
    tie_key: str
    size: int
    preferences: list[Preference]


def _team_members(team: Team) -> list[Student]:
    return [membership.student for membership in team.members if membership.student is not None]


def _sync_team_leader(team: Team) -> Student | None:
    members = _team_members(team)
    if not members:
        team.leader_student_id = None
        return None
    leader = sorted(members, key=lambda student: (-student.average_grade, student.album_number, student.id))[0]
    team.leader_student_id = leader.id
    return leader


def run_assignment(db: Session, selection_round_id: int) -> tuple[list[Assignment], list[dict[str, object]]]:
    selection_round = db.get(SelectionRound, selection_round_id)
    if selection_round is None:
        raise ValueError("selection round not found")

    db.execute(delete(Assignment).where(Assignment.selection_round_id == selection_round_id))

    supervisors = db.execute(select(Supervisor).order_by(Supervisor.id)).scalars().all()
    remaining_capacity = {supervisor.id: supervisor.capacity for supervisor in supervisors}

    preferences = (
        db.execute(
            select(Preference)
            .where(Preference.selection_round_id == selection_round_id)
            .order_by(Preference.priority, Preference.id)
        )
        .scalars()
        .all()
    )
    grouped_preferences: dict[tuple[str, int], list[Preference]] = {}
    for preference in preferences:
        if preference.student_id is not None:
            key = ("student", preference.student_id)
        else:
            key = ("team", preference.team_id)
        grouped_preferences.setdefault(key, []).append(preference)

    team_memberships = db.execute(select(TeamMember)).scalars().all()
    students_in_teams = {membership.student_id for membership in team_memberships}

    candidates: list[Candidate] = []
    unassigned: list[dict[str, object]] = []

    for (actor_type, actor_id), actor_preferences in grouped_preferences.items():
        if actor_type == "student":
            if actor_id in students_in_teams:
                unassigned.append({"actor_type": actor_type, "actor_id": actor_id, "reason": "student_belongs_to_team"})
                continue
            student = db.get(Student, actor_id)
            if student is None:
                unassigned.append({"actor_type": actor_type, "actor_id": actor_id, "reason": "student_not_found"})
                continue
            candidates.append(
                Candidate(
                    actor_type=actor_type,
                    actor_id=actor_id,
                    score=student.average_grade,
                    tie_key=student.album_number,
                    size=1,
                    preferences=sorted(actor_preferences, key=lambda item: (item.priority, item.id)),
                )
            )
            continue

        team = db.get(Team, actor_id)
        if team is None:
            unassigned.append({"actor_type": actor_type, "actor_id": actor_id, "reason": "team_not_found"})
            continue
        leader = _sync_team_leader(team)
        if leader is None:
            unassigned.append({"actor_type": actor_type, "actor_id": actor_id, "reason": "team_has_no_members"})
            continue
        candidates.append(
            Candidate(
                actor_type=actor_type,
                actor_id=actor_id,
                score=leader.average_grade,
                tie_key=team.name,
                size=len(_team_members(team)),
                preferences=sorted(actor_preferences, key=lambda item: (item.priority, item.id)),
            )
        )

    assignments: list[Assignment] = []
    for candidate in sorted(candidates, key=lambda item: (-item.score, item.tie_key, item.actor_id)):
        selected_preference = None
        for preference in candidate.preferences:
            if remaining_capacity.get(preference.supervisor_id, 0) >= candidate.size:
                selected_preference = preference
                break
        if selected_preference is None:
            unassigned.append(
                {
                    "actor_type": candidate.actor_type,
                    "actor_id": candidate.actor_id,
                    "reason": "no_supervisor_capacity_for_preferences",
                }
            )
            continue

        remaining_capacity[selected_preference.supervisor_id] -= candidate.size
        assignment = Assignment(
            selection_round_id=selection_round_id,
            student_id=candidate.actor_id if candidate.actor_type == "student" else None,
            team_id=candidate.actor_id if candidate.actor_type == "team" else None,
            supervisor_id=selected_preference.supervisor_id,
            assignment_source=f"preference_{selected_preference.priority}",
        )
        if candidate.actor_type == "team":
            team = db.get(Team, candidate.actor_id)
            if team is not None:
                team.assigned_supervisor_id = selected_preference.supervisor_id
        db.add(assignment)
        assignments.append(assignment)

    selection_round.status = RoundStatus.assigned
    db.commit()
    for assignment in assignments:
        db.refresh(assignment)
    return assignments, unassigned
