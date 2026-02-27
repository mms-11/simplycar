
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead
from app.api.services.users_service import create_user, get_user_by_login
from app.core.database import get_db
from app.utils.security import verify_password
from app.utils.jwt_auth import create_access_token

router = APIRouter()


@router.post("/", response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_login(db, user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="Login already registered")
    return create_user(db, user)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_login(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect login or password")
    access_token = create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}



