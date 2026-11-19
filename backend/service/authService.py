from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.config.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    SECRET_KEY,
)
from backend.models.user import User

passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashPassword(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password must be 72 bytes or fewer.")
    return passwordContext.hash(password)


def verifyPassword(password: str, hashedPassword: str) -> bool:
    try:
        if len(password.encode("utf-8")) > 72:
            return False
        return passwordContext.verify(password, hashedPassword)
    except (ValueError, TypeError):
        return False


def createAccessToken(data: dict) -> str:
    toEncode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    toEncode.update({"exp": expire})
    return jwt.encode(toEncode, SECRET_KEY, algorithm=JWT_ALGORITHM)


def registerUser(db: Session, name: str, email: str, password: str):
    normalizedEmail = email.strip().lower()
    existingUser = db.query(User).filter(func.lower(User.email) == normalizedEmail).first()
    if existingUser:
        return None

    user = User(
        name=name.strip(),
        email=normalizedEmail,
        password_hash=hashPassword(password),
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        return None

    token = createAccessToken({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
    }


def loginUser(db: Session, email: str, password: str):
    normalizedEmail = email.strip().lower()
    user = db.query(User).filter(func.lower(User.email) == normalizedEmail).first()
    if not user or not verifyPassword(password, user.password_hash):
        return None

    token = createAccessToken({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
    }


def decodeToken(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        userId = payload.get("sub")
        return int(userId) if userId is not None else None
    except (JWTError, TypeError, ValueError):
        return None
