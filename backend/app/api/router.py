from fastapi import APIRouter

from app.api.routes.assignments import router as assignments_router
from app.api.routes.demo import router as demo_router
from app.api.routes.health import router as health_router
from app.api.routes.overview import router as overview_router
from app.api.routes.preferences import router as preferences_router
from app.api.routes.rounds import router as rounds_router
from app.api.routes.students import router as students_router
from app.api.routes.supervisors import router as supervisors_router
from app.api.routes.teams import router as teams_router
from app.api.routes.users import router as users_router


api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(overview_router, prefix="/overview", tags=["overview"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(students_router, prefix="/students", tags=["students"])
api_router.include_router(supervisors_router, prefix="/supervisors", tags=["supervisors"])
api_router.include_router(teams_router, prefix="/teams", tags=["teams"])
api_router.include_router(rounds_router, prefix="/rounds", tags=["rounds"])
api_router.include_router(preferences_router, prefix="/preferences", tags=["preferences"])
api_router.include_router(assignments_router, prefix="/assignments", tags=["assignments"])
api_router.include_router(demo_router, prefix="/demo", tags=["demo"])
