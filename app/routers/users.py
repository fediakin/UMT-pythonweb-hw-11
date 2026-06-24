from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.auth import get_current_user
from app.services.avatar import upload_avatar

router = APIRouter(prefix="/users", tags=["Users"])

# Обмеження: не більше 5 запитів на хвилину
@router.get("/me", response_model=UserResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/avatar", response_model=UserResponse)
async def update_avatar(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Використовуємо email як унікальне ім'я для файлу в Cloudinary
    public_id = f"contacts_app/{current_user.email}"
    avatar_url = upload_avatar(file, public_id)
    
    current_user.avatar = avatar_url
    db.commit()
    db.refresh(current_user)
    return current_user