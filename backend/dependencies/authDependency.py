from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.models.user import User
from backend.service.authService import decodeToken

security = HTTPBearer(auto_error=False)


def getCurrentUser(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
):
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required or token is invalid.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized

    userId = decodeToken(credentials.credentials)
    if userId is None:
        raise unauthorized

    user = db.query(User).filter(User.id == userId).first()
    if user is None:
        raise unauthorized
    return user
