from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.security import hash_password
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models import *

from app.api.routes import auth, users, students, supervisors, topics, teams, preferences, selection_rounds, assignments
from app.models.user import User, UserRole

app = FastAPI(
    title="System Wyboru Promotorów",
    description="API do zarządzania procesem wyboru promotorów prac dyplomowych",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(students.router, prefix="/api")
app.include_router(supervisors.router, prefix="/api")
app.include_router(topics.router, prefix="/api")
app.include_router(teams.router, prefix="/api")
app.include_router(preferences.router, prefix="/api")
app.include_router(selection_rounds.router, prefix="/api")
app.include_router(assignments.router, prefix="/api")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    _seed_admin()

def _seed_admin():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.role == UserRole.ADMIN).first()
        if not existing:
            admin = User(
                email=settings.ADMIN_EMAIL,
                password_hash=hash_password(settings.ADMIN_PASSWORD),
                first_name="Admin",
                last_name="System",
                role=UserRole.ADMIN,
                is_active=True,
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "System Wyboru Promotorów API", "Docs": "/docs"}