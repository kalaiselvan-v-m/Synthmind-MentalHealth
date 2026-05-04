from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend.models.user import User

SECRET_KEY = "CHANGE_THIS_SECRET_KEY_LATER"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashPassword(password: str):
    return passwordContext.hash(password)


def verifyPassword(password: str, hashedPassword: str):
    return passwordContext.verify(password, hashedPassword)


def createAccessToken(data: dict):
    toEncode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    toEncode.update({"exp": expire})

    return jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)


def registerUser(db: Session, name: str, email: str, password: str):
    existingUser = db.query(User).filter(User.email == email).first()

    if existingUser:
        return None

    user = User(
        name=name,
        email=email,
        password_hash=hashPassword(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = createAccessToken({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }


def loginUser(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verifyPassword(password, user.password_hash):
        return None

    token = createAccessToken({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }


def decodeToken(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userId = payload.get("sub")

        if userId is None:
            return None

        return int(userId)

    except JWTError:
        return None