from fastapi import APIRouter,status,Depends,HTTPException
from app.services import user_service
from app.schemas import users_schemas
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.init_db import get_db

router  = APIRouter(
    tags=["Users"],
    prefix="/users",
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(request: users_schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    user = await user_service.create_user(request, db)
    if not user:
        raise HTTPException(status_code=400, detail="User creation failed")
    raise HTTPException(status_code=201, detail="User created successfully")

@router.get("/{user_id}", response_model=users_schemas.ShowUser, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_user(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


