from pydantic import BaseModel,field_validator
from datetime import datetime
from enum import Enum 



class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    title: str
    description: str
    priority : Priority
    
    @field_validator('priority')
    def validate_priority(cls, value):
        if value not in Priority.__members__:
            raise ValueError('Invalid priority value')
        return value


class ShowTask(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    priority : str
    user_id:int

    class Config:
        from_attributes = True        