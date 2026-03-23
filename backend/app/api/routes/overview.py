from fastapi import APIRouter


router = APIRouter()


@router.get("")
def get_overview() -> dict[str, object]:
    return {
        "project": "System Wyboru Promotorow",
        "stage": 1,
        "stack": {
            "backend": "FastAPI",
            "frontend": "React + TypeScript",
            "database": "PostgreSQL",
        },
        "modules": [
            "authentication",
            "users",
            "teams",
            "preferences",
            "assignment",
            "reports",
        ],
    }
