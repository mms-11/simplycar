from sqlalchemy.orm import Session
from ..database.connection import get_db

def get_database_session() -> Session:
    yield from get_db()