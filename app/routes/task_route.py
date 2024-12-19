from fastapi import APIRouter,status,Depends,HTTPException
from app.services import task_service
from app.schemas import tasks_schemas
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.init_db import get_db
from typing import List
from app.core.security import get_current_user
from app.schemas.tokens_schema import TokenData
from typing import Annotated,Optional
                    
                    
router = APIRouter(
    tags=["Tasks"],
    prefix="/tasks",
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(request: tasks_schemas.TaskCreate, db: AsyncSession = Depends(get_db), current_user:TokenData = Depends(get_current_user)):
    
    task = await task_service.create_task(request, db, current_user.username)
    if not task:
        raise HTTPException(status_code=400, detail="Task creation failed")
    raise HTTPException(status_code=201, detail="Task created successfully")

@router.get("/", response_model=List[tasks_schemas.ShowTask] ,status_code=status.HTTP_200_OK)
async def get_tasks(db: AsyncSession = Depends(get_db),current_user:TokenData = Depends(get_current_user),sorting :Optional[str] = None):
    
    tasks = await task_service.get_tasks(db,current_user.username,sorting)
    return tasks


@router.get("/{task_id}", response_model=tasks_schemas.ShowTask, status_code=status.HTTP_200_OK)  
async def get_tasks(task_id:int, db: AsyncSession = Depends(get_db),current_user:TokenData = Depends(get_current_user)):
    task = await task_service.get_task(task_id, db,current_user.username)
    if task:
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")


@router.put("/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(task_id: int, request: tasks_schemas.TaskCreate, db: AsyncSession = Depends(get_db),current_user:TokenData = Depends(get_current_user)):
    task = await task_service.update_task(task_id, request, db,current_user.username)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        raise HTTPException(status_code=200, detail="Task updated successfully")
    
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db),current_user:TokenData = Depends(get_current_user)):
    task = await task_service.delete_task(task_id, db,current_user.username)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        raise HTTPException(status_code=204, detail="Task deleted successfully")