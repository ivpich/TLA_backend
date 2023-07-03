from typing import List
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.utils.file_utils import save_upload_file
from app.models.user import User as UserModel, User
from app.core.auth import verify_init_data
from app.core.database import get_db
from app.models.user_update import UserUpdate
from fastapi import UploadFile, File

router = APIRouter()


def get_user_by_chat_id(db, chat_id):
    return db.query(User).filter(User.chat_id == chat_id).first()


@router.get("/get-me", response_model=UserModel)
async def get_me(init_data: str = Header(None), db: Session = Depends(get_db)):
    chat_id = verify_init_data(init_data)
    if chat_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = get_user_by_chat_id(db, chat_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/update-profile", response_model=UserModel)
async def update_profile(user_update: UserUpdate, init_data: str = Header(None), db: Session = Depends(get_db)):
    chat_id = verify_init_data(init_data)
    if chat_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = get_user_by_chat_id(db, chat_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.name is not None:
        user.name = user_update.name
    if user_update.description is not None:
        user.description = user_update.description
    db.commit()
    return user


@router.post("/upload-profile-photo", response_model=UserModel)
async def upload_profile_photo(profile_photo: UploadFile = File(...), init_data: str = Header(None),
                               db: Session = Depends(get_db)):
    chat_id = verify_init_data(init_data)
    if chat_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = get_user_by_chat_id(db, chat_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    filename = save_upload_file(profile_photo, directory="profile_photos")
    user.profile_photo = filename
    db.commit()
    return user
