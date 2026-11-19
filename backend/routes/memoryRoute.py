from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User
from backend.models.userMemory import UserMemory

router = APIRouter(prefix="/memory", tags=["Memory"])


@router.get("")
def get_memories(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser),
):
    memories = (
        db.query(UserMemory)
        .filter(UserMemory.user_id == currentUser.id)
        .order_by(UserMemory.importance.desc())
        .all()
    )
    return [
        {
            "id": item.id,
            "type": item.memory_type,
            "key": item.memory_key,
            "value": item.memory_value,
            "importance": item.importance,
            "created_at": item.created_at,
        }
        for item in memories
    ]


@router.delete("/{memory_id}")
def delete_memory(
    memory_id: int,
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser),
):
    memory = (
        db.query(UserMemory)
        .filter(UserMemory.id == memory_id, UserMemory.user_id == currentUser.id)
        .first()
    )
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    db.delete(memory)
    db.commit()
    return {"message": "Memory deleted"}


@router.delete("")
def clear_memories(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser),
):
    db.query(UserMemory).filter(UserMemory.user_id == currentUser.id).delete(synchronize_session=False)
    db.commit()
    return {"message": "All memories cleared"}
