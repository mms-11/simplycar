from sqlalchemy.orm import Session
from app.models.user import User, UserType
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash


def get_user_by_login(db: Session, login: str):
    return db.query(User).filter(User.login == login).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        login=user.login,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        type=user.type,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def update_user(db: Session, user_id: int, user_update: UserCreate):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.login = user_update.login
        user.email = user_update.email
        user.hashed_password = get_password_hash(user_update.password)
        user.type = user_update.type
        db.commit()
        db.refresh(user)
        return user
    return None


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()    


