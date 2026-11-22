import jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from db_models import UserDB
from security import oauth2_scheme, SECRET_KEY, ALGORITHM

def get_app_info():
    return {
        "app_name": "Student Management API",
        "version": "1.0.0"
    }

def get_student_not_found():
    return {
        "error": "Student not found",
        "message": "The requested student does not exist."
    }

class StudentNotFoundException(Exception):
    pass

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except jwt.InvalidTokenError:
        raise credentials_exception

    user = db.query(UserDB).filter(
        UserDB.username == username
    ).first()

    if user is None:
        raise credentials_exception

    return user