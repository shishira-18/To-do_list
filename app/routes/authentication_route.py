from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from app.database.init_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemas import tokens_schema,users_schemas
from app.core.token import create_access_token,create_refresh_token,verify_refresh_token
from app.core.hashing import Hasher
from sqlalchemy import select


router  = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/refresh-token",response_model=tokens_schema.Token)
async def refresh_token(refresh_token:str,db:AsyncSession=Depends(get_db)):
    
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Refresh Token Required")
    if not verify_refresh_token(refresh_token,credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Refresh Token")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Refresh Token")
    return verify_refresh_token(refresh_token,credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Refresh Token"))

@router.post("/login",response_model=tokens_schema.Token)
async def login(request:OAuth2PasswordRequestForm=Depends(),db:AsyncSession=Depends(get_db)):

    result = await db.execute(select(User).where(User.username == request.username))  # Correct query
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not Hasher.verify_password(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")

    access_token = create_access_token(data={"username":user.username})
    refresh_token = create_refresh_token(data={"username":user.username})
    return {"access_token":access_token,"refresh_token":refresh_token,"token_type":"bearer"}    



@router.post("/reset_password",status_code=status.HTTP_200_OK)
async def reset_password(request:users_schemas.ResetPassword,db:AsyncSession=Depends(get_db)):
    user = await db.execute(select(User).where(User.username == request.username))
    user = user.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not Hasher.verify_password(request.old_password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    user.password = Hasher.get_password_hash(request.new_password)
    await db.commit()
    return {"message":"Password reset successfully"}

    
    
    