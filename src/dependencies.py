from fastapi import Depends
from sqlalchemy.orm import Session
from src.database import get_db


def get_db_session():
    return Depends(get_db)