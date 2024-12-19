from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,case
from app.models.tasks_model import Task
from app.models.users_model import User
from datetime import datetime


async def  _get_user(db: AsyncSession, current_user):
    user = await db.execute(select(User).where(User.username == current_user))
    return user.scalars().first()

async def get_tasks(db: AsyncSession, current_user, sorting):
    
    user = await _get_user(db, current_user)
    if user is None:
        return []
    priority_order = case(
            {
                "low": 1,
                "medium": 2,
                "high": 3
            },
            value=Task.priority
        )
    if sorting == "asc":
        
        
        tasks = await db.execute(select(Task).where(Task.user_id == user.id).order_by(priority_order.asc()))
        
        
        
        
    else:
        tasks = await db.execute(select(Task).where(Task.user_id == user.id).order_by(priority_order.desc()))
    return tasks.scalars().all()

async def create_task(task_data: dict, db: AsyncSession, current_user):
    print(current_user)
    user = await _get_user(db, current_user) 
    if user is None:
        return None

    task = Task(
        title=getattr(task_data, "title", None),
        description=getattr(task_data, "description", None),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        priority = getattr(task_data, "priority", "medium"),
        user_id=user.id,
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_task(task_id: int, db: AsyncSession, current_user):
    user = await _get_user(db, current_user)
    if not user:
        return None
    
    task = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == user.id))
    return task.scalars().first()

async def update_task(task_id: int, task_data: dict, db: AsyncSession, current_user):
    
    
    user = await _get_user(db, current_user)
    if not user:
        return None
    
    task = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == user.id))
    task = task.scalars().first()
    if task:
        task.title = task_data.title
        task.description = task_data.description
        task.priority = task_data.priority
        task.updated_at = datetime.now()
        await db.commit()
        await db.refresh(task)
        return task
    else:
        return None


async def delete_task(task_id: int, db: AsyncSession, current_user):
    # task = await db.execute(select(Task).where(Task.id == task_id))
    
    user = await _get_user(db, current_user)
    if not user:
        return None
    task = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == user.id))
    task = task.scalars().first()
    if task:
        await db.delete(task)
        await db.commit()
        return task
    else:
        return None
