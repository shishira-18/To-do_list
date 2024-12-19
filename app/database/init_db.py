from app.database.base import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users_model import User
from app.core.config import settings
from sqlalchemy import select
from app.core.hashing import Hasher
async def create_default_user(db: AsyncSession):
    result = await db.execute(select(User).filter(User.role == "admin"))
    admin = result.scalars().first()
    
    if not admin:
        admin = User(
            username=settings.ADMIN_USERNAME, 
            email=settings.ADMIN_EMAIL, 
            password=Hasher.get_password_hash(settings.ADMIN_PASSWORD), 
            role="admin"
        )
        db.add(admin)
        await db.commit()
        await db.refresh(admin)
        print(f"Admin user created: {admin.username}")
        

async def get_db():
    async with async_session() as session:
        yield session
        