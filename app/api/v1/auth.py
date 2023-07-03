from email.header import Header

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.core.auth import create_init_data, verify_init_data
from app.core.database import SessionLocal, get_db
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()


# Define a model for the user's input
class UserLoginInput(BaseModel):
    chat_id: int
    name: str


@router.post("/login")
async def login(user_input: UserLoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.chat_id == user_input.chat_id).first()

    if not user:
        # User does not exist, let's create it
        user = User(chat_id=user_input.chat_id, name=user_input.name)
        db.add(user)
        db.commit()
    elif user.wallet:
        raise HTTPException(status_code=400, detail="User with this chat_id already exists")

    # At this point, we have a User instance whether it was retrieved or created

    init_data = create_init_data(user.chat_id)
    return {"init_data": init_data, "id": user.id, "wallet": user.wallet, "chat_id": user.chat_id, "name": user.name}
