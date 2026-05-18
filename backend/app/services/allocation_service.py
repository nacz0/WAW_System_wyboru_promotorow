from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.supervisor import Supervisor
from app.models.team import Team
from app.models.assignment import Assignment
from app.models.preference import Preference
from app.models.selection_round import SelectionRound, RoundStatus

def run_allocation(db: Session, round_id: int) -> dict:
    selection_round = db.get(SelectionRound, round_id)
    if not selection_round:
        return {"error": "Selection round not found"}
    if selection_round.status != RoundStatus.CLOSED:
        return {"error": "Selection round must be in 'CLOSED' status to run allocation"}
    
    #Clear any existing allocations for this round
    db.query(Assignment).filter(Assignment.round_id == round_id).delete()

    #Load all preferences for this round
    all_preferences = (
        db.query(Preference)
        .filter(Preference.selection_round_id == round_id)
        .order_by(Preference.priority)
        .all()
    )

    #Build allocation entries: each in either individual student or team
    entries: list[dict] = []
    processed_student_ids: set[int] = set()
    processed_team_ids: set[int] = set()

    for pref in all_preferences:
        if pref.student_id and pref.student_id not in processed_student_ids:
            student = db.get(Student, pref.student_id)
            if student:
                processed_student_ids.add(student.id)
                entries.append({
                    "type": "student",
                    "student_id": student.id,
                    "team_id": None,
                    "sort_grade": student.average_grade,
                    "sort_tiebreaker": student.album_number,
                })
        elif pref.team_id and pref.team_id not in processed_team_ids:
            team = db.get(Team, pref.team_id)
            if team:
                processed_team_ids.add(team.id)
                leader = max(team.members, key=lambda s: (s.average_grade, s.album_number))
                entries.append({
                    "type": "team",
                    "student_id": None,
                    "team_id": team.id,
                    "sort_grade": leader.average_grade,
                    "sort_tiebreaker": leader.album_number,
                })

    #Sort: descending by grade, ascending by album number for tiebreaker
    entries.sort(key=lambda e: (-e["sort_grade"], e["sort_tiebreaker"]))

    #Track remaining capacities for supervisors
    supervisors = db.query(Supervisor).all()
    capacity_map: dict[int, int] = {sup.id: sup.capacity for sup in supervisors}

    assigned_count = 0
    unassigned: list[dict] = []

    for entry in entries:
        if entry["type"] == "student":
            prefs = sorted(
                [p for p in all_preferences if p.student_id == entry["student_id"]],
                key=lambda p: p.priority
            )
        else:
            prefs = sorted(
                [p for p in all_preferences if p.team_id == entry["team_id"]],
                key=lambda p: p.priority
            )

        assigned = False
        slots_needed = 1 
        if entry["type"] == "team":
            team = db.get(Team, entry["team_id"])
            slots_needed = len(team.members) if team else 1
        for pref in prefs:
            if capacity_map.get(pref.supervisor_id, 0) >= slots_needed:
                assignment = Assignment(
                    selection_round_id=round_id,
                    student_id=entry["student_id"],
                    team_id=entry["team_id"],
                    supervisor_id=pref.supervisor_id,
                    assignment_source=f"preference_{pref.priority}"
                )
                db.add(assignment)
                capacity_map[pref.supervisor_id] -= slots_needed

                if entry["type"] == "team" and team:
                    team.assigned_supervisor_id = pref.supervisor_id

                assigned = True
                assigned_count += 1
                break
        if not assigned:
            unassigned.append(entry)

    selection_round.status = RoundStatus.COMPLETED
    db.commit()

    return {
        "assigned": assigned_count,
        "unassigned": len(unassigned),
        "unassigned_details": [
            {"type": e["type"], "student_id": e["student_id"], "team_id": e["team_id"]} for e in unassigned
        ],
    }