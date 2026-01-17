from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app. models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Service for user operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()

    def create(self, user_in: UserCreate) -> User:
        """Create a new user."""
        user = User(
            email=user_in.email,
            username=user_in.username,
            full_name=user_in. full_name,
            hashed_password=get_password_hash(user_in.password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user:  User, user_in: UserUpdate) -> User:
        """Update a user."""
        update_data = user_in.model_dump(exclude_unset=True)
        for field, value in update_data. items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user."""
        user = self. get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def add_xp(self, user: User, xp: int) -> tuple[User, bool]:
        """Add XP to user, returns (user, leveled_up)."""
        user.xp += xp
        old_level = user.level
        user. level = self._calculate_level(user.xp)
        self.db.commit()
        self.db.refresh(user)
        return user, user.level > old_level

    def _calculate_level(self, xp: int) -> int:
        """Calculate level from XP.  Simple formula: level = 1 + floor(sqrt(xp / 100))"""
        import math
        return 1 + int(math.sqrt(xp / 100))