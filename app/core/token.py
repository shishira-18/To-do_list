from datetime import timedelta,datetime,timezone
import jwt
from jwt.exceptions import InvalidTokenError
from app.schemas  import tokens_schema
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTE = settings.ACCESS_TOKEN_EXPIRE_MINUTE
REFRESH_TOKEN_EXPIRE_MINUTE = settings.REFRESH_TOKEN_EXPIRE_MINUTE



def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp":expire})
    encoded_jwt =  jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTE)  # Refresh tokens typically last longer
    to_encode.update({"exp":expire, "token_type": "refresh"})  # Add token type identifier
    encoded_jwt =  jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt



def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get("username")
        print(username)
        if username is None:
            raise credentials_exception
        token_data = tokens_schema.TokenData(username=username)
        return token_data
    except InvalidTokenError:
        return None

def verify_refresh_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        token_type: str = payload.get("token_type")
        if username is None or token_type != "refresh":
            raise credentials_exception
        
        # Generate new tokens
        access_token = create_access_token({"username": username})
        refresh_token = create_refresh_token({"username": username})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except InvalidTokenError:
        return None