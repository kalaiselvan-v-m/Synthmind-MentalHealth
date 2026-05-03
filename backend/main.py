from fastapi import FastAPI
from backend.config.database import Base, engine
from backend.routes.authRoute import router as auth_router

app = FastAPI(title="SynthMind API")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/")
def home():
    return {"message": "SynthMind Running"}