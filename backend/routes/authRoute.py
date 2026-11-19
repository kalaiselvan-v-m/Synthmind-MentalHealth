from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.schemas.authSchema import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
)
from backend.service.authService import loginUser, registerUser

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        result = registerUser(
            db=db,
            name=data.name,
            email=str(data.email),
            password=data.password,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    if not result:
        raise HTTPException(status_code=409, detail="Email already registered")
    return result


@router.post("/login", response_model=AuthResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    result = loginUser(
        db=db,
        email=str(data.email),
        password=data.password,
    )
    if not result:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return result
