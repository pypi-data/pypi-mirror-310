from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Type
from FastAuthX.database import get_db
from FastAuthX.auth_token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    user_model: Type = None,  # Pass user model dynamically
    query_pattern: str = "username",  # Default query field
):
    """
    Returns the current authenticated user based on the token.
    """
    if not user_model:
        raise ValueError("User model must be provided.")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token)
    query = {query_pattern: token_data.username}
    user = db.query(user_model).filter_by(**query).first()

    if not user:
        raise credentials_exception

    return user
