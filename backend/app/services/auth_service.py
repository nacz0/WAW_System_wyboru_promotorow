from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import verify_password, create_access_token, hash_password

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    # email parameter can come from OAuth2PasswordRequestForm.username field
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    if not user.is_active:
        return None
    return user

def create_token_for_user(user: User) -> str:
    return create_access_token(data={"sub": str(user.id), "role": user.role.value})