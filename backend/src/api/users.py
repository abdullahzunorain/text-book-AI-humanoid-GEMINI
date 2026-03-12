from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.db.crud_users import create_user, get_user_by_id, get_user_by_email
from src.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_user = await create_user(
            db,
            name=user.name,
            email=user.email,
            hardware_background=user.hardware_background,
            software_background=user.software_background,
        )
        return db_user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")


@router.get("/users/lookup", response_model=UserResponse)
async def lookup_user(email: str, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
