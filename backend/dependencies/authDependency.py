from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.models.user import User
from backend.service.authService import decodeToken

security = HTTPBearer()


def getCurrentUser(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    userId = decodeToken(token)

    if not userId:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == userId).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user