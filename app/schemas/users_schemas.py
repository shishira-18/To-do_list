from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
class ShowUser(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True  # New Pydantic v2 syntax (replaces orm_mode)
        
class ResetPassword(BaseModel):
    username: str
    old_password: str
    new_password: str
        
