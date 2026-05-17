from fastapi import APIRouter


router = APIRouter()


@router.get("")
def get_overview() -> dict[str, object]:
    return {
        "project": "System Wyboru Promotorow",
        "stage": 2,
        "stack": {
            "backend": "FastAPI",
            "frontend": "React + TypeScript",
            "database": "PostgreSQL",
        },
        "modules": [
            "auth",
            "users",
            "students",
            "supervisors",
            "teams",
            "selection_rounds",
            "preferences",
            "assignments",
            "reports",
        ],
    }
