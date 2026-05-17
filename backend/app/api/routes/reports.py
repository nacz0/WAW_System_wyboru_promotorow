import csv
from io import StringIO

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.db.session import get_db
from app.models import Assignment, SelectionRound, Student, Supervisor, Team, User, UserRole


router = APIRouter()


def _student_label(student: Student | None) -> str:
    if student is None or student.user is None:
        return ""
    return f"{student.user.first_name} {student.user.last_name} ({student.album_number})"


def _supervisor_label(supervisor: Supervisor | None) -> str:
    if supervisor is None or supervisor.user is None:
        return ""
    return f"{supervisor.user.first_name} {supervisor.user.last_name}"


def _assignment_actor_label(assignment: Assignment) -> str:
    if assignment.student_id is not None:
        return _student_label(assignment.student)
    if assignment.team is None:
        return ""
    members = ", ".join(_student_label(member.student) for member in assignment.team.members)
    return f"{assignment.team.name}: {members}"


@router.get("/assignments.csv")
def export_assignments_csv(
    selection_round_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.admin)),
) -> Response:
    query = select(Assignment).order_by(Assignment.selection_round_id, Assignment.id)
    if selection_round_id is not None:
        query = query.where(Assignment.selection_round_id == selection_round_id)

    output = StringIO()
    output.write("sep=;\n")
    writer = csv.writer(output, delimiter=";", lineterminator="\n")
    writer.writerow(
        [
            "selection_round_id",
            "selection_round_name",
            "actor_type",
            "actor",
            "supervisor",
            "assignment_source",
            "assigned_at",
        ]
    )

    for assignment in db.execute(query).scalars().all():
        selection_round = db.get(SelectionRound, assignment.selection_round_id)
        actor_type = "student" if assignment.student_id is not None else "team"
        writer.writerow(
            [
                assignment.selection_round_id,
                selection_round.name if selection_round is not None else "",
                actor_type,
                _assignment_actor_label(assignment),
                _supervisor_label(assignment.supervisor),
                assignment.assignment_source,
                assignment.assigned_at.isoformat(),
            ]
        )

    filename = "assignments.csv"
    if selection_round_id is not None:
        filename = f"assignments-round-{selection_round_id}.csv"
    return Response(
        content="\ufeff" + output.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
