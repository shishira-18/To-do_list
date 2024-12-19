from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Enum as SqlaclchemyEnum
from sqlalchemy.orm import relationship
from app.database.base import base
from enum import Enum

class Role(Enum):
    USER = "user"
    ADMIN  = "admin"
    

class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True)  # Added length specification
    email = Column(String(255), unique=True)  # Added length specification
    password = Column(String(255))  # Added length specification
    role = Column(SqlaclchemyEnum(Role))
    tasks = relationship("Task", back_populates="user")
    