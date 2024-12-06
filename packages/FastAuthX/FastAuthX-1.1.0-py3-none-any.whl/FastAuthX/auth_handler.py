from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from .auth_token import create_access_token, verify_token
from .hashing import Hash
from .schemas import Token
from .database import get_db
from .oauth2 import oauth2_scheme
from typing import Type


class AuthHandler:
    def __init__(
        self,
        model: Type,
        query_pattern: str = "username",
        token_expiry_minutes: int = 15,
        refresh_expiry_days: int = 7,
        secret_key: str = "default-secret-key",
        algorithm: str = "HS256",
    ):
        self.model = model
        self.query_pattern = query_pattern
        self.token_expiry_minutes = token_expiry_minutes
        self.refresh_expiry_days = refresh_expiry_days
        self.secret_key = secret_key
        self.algorithm = algorithm

    def login(self, request, db: Session) -> Token:
        user = db.query(self.model).filter(
            getattr(self.model, self.query_pattern) == getattr(request, self.query_pattern)
        ).first()
        if not user or not Hash.verify(user.password, request.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        access_token = create_access_token(
            data={"sub": getattr(user, self.query_pattern)},
            secret_key=self.secret_key,
            algorithm=self.algorithm,
            expiry_minutes=self.token_expiry_minutes,
        )
        return Token(access_token=access_token, token_type="bearer")

    def signup(self, request, db: Session):
        if db.query(self.model).filter(
            getattr(self.model, self.query_pattern) == getattr(request, self.query_pattern)
        ).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{self.query_pattern} already registered",
            )
        hashed_password = Hash.bcrypt(request.password)
        new_user = self.model(**request.dict(), password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully"}

    def get_current_user(self, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
        token_data = verify_token(
            token, self.secret_key, self.algorithm
        )  # Handles token decoding & validation
        user = db.query(self.model).filter(
            getattr(self.model, self.query_pattern) == token_data.username
        ).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        return user
