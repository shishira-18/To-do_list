from app.models.users_model import User
from app.schemas import users_schemas
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.hashing import Hasher

async def create_user(request: users_schemas.UserCreate, db: AsyncSession):
    
    try:
        user = User(username=request.username, email=request.email, password=Hasher.get_password_hash(request.password))
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except Exception as e:
        print(e)
        await db.rollback()
        return None 
       
async def get_user(user_id: int, db: AsyncSession):
    user = await db.get(User, user_id)
    return user
