import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
# Update this import based on your project structure
from schemas import user_schema
from passlib.context import CryptContext
from dependencies import database

# Secret key to encode and decode JWT tokens
SECRET_KEY = "SID8493"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = user_schema.TokenData(username=username)
        
        user = database.get_user_by_id(
            database.get_user_id(token_data.username))
        # return user_schema.UserPublic(user)
        return user
    except JWTError:
        
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)


def get_password_hash(password: str) -> str:
    
    hashed_password = pwd_context.hash(password)
    
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    verification_result = pwd_context.verify(plain_password, hashed_password)
    return verification_result


