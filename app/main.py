from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import authentication_route, task_route, users_route
from app.database.base import base, engine
from app.database.base import async_session

from app.database.init_db import create_default_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)
    async with async_session() as session:
        await create_default_user(session)
    yield
    await engine.dispose()

app = FastAPI(
    title="Task Management System",
    description="A simple task management system built with FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",lifespan=lifespan)



app.include_router(authentication_route.router)
app.include_router(task_route.router)
app.include_router(users_route.router)