from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.schemas.authSchema import RegisterRequest, LoginRequest
from backend.service.authService import registerUser, loginUser

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    result = registerUser(
        db=db,
        name=data.name,
        email=data.email,
        password=data.password
    )

    if not result:
        raise HTTPException(status_code=400, detail="Email already registered")

    return result


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    result = loginUser(
        db=db,
        email=data.email,
        password=data.password
    )

    if not result:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return result