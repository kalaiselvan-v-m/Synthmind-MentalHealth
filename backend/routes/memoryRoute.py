from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.models.userMemory import UserMemory

router = APIRouter(prefix="/memory", tags=["Memory"])


# ✅ Get all memories for a user
@router.get("/{user_id}")
def get_memories(user_id: int, db: Session = Depends(get_db)):
    memories = (
        db.query(UserMemory)
        .filter(UserMemory.user_id == user_id)
        .order_by(UserMemory.importance.desc())
        .all()
    )

    return [
        {
            "id": m.id,
            "type": m.memory_type,
            "key": m.memory_key,
            "value": m.memory_value,
            "importance": m.importance,
            "created_at": m.created_at
        }
        for m in memories
    ]


# ✅ Delete a single memory
@router.delete("/{memory_id}")
def delete_memory(memory_id: int, db: Session = Depends(get_db)):
    memory = db.query(UserMemory).filter(UserMemory.id == memory_id).first()

    if not memory:
        return {"message": "Memory not found"}

    db.delete(memory)
    db.commit()

    return {"message": "Memory deleted"}


# ✅ Clear all memories for a user
@router.delete("/clear/{user_id}")
def clear_memories(user_id: int, db: Session = Depends(get_db)):
    db.query(UserMemory).filter(UserMemory.user_id == user_id).delete()
    db.commit()

    return {"message": "All memories cleared"}