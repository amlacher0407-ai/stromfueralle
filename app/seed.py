from app.config import settings
from app.database import SessionLocal
from app.models.user import User
from app.security import hash_password


def seed_admin() -> None:
    db = SessionLocal()
    try:
        if not db.query(User).first():
            admin = User(
                username=settings.admin_username,
                password_hash=hash_password(settings.admin_default_password),
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()
