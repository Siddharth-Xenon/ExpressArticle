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

print("authenticating...")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    print("Creating access token...")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Token data: {to_encode}")
    print(f"Encoded JWT: {encoded_jwt}")
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        print(f"Verifying token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded payload: {payload}")
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = user_schema.TokenData(username=username)
        print("Token verified")
        user = database.get_user_by_id(
            database.get_user_id(token_data.username))
        # return user_schema.UserPublic(user)
        return user
    except JWTError:
        print("Token verification failed")
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    print(f"Retrieving current user with token: {token}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)


def get_password_hash(password: str) -> str:
    print(f"Hashing password: {password}")
    hashed_password = pwd_context.hash(password)
    print(f"Hashed password: {hashed_password}")
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    print(
        f"Verifying password: {plain_password} against hash: {hashed_password}")
    verification_result = pwd_context.verify(plain_password, hashed_password)
    print(f"Password verification result: {verification_result}")
    return verification_result


# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# def verify_token(token: str, credentials_exception):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         print("token verified")
#         return user_schema.UserPublic(username=username)
#     except JWTError:  # Changed from JWTError to PyJWTError
#         print("token not verified")
#         raise credentials_exception


# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     print("token: ", token)
#     return verify_token(token, credentials_exception)

# # Additional authentication/authorization methods can be added as needed


# def get_password_hash(password: str) -> str:
#     """
#     Hash a password for storing.
#     """
#     return pwd_context.hash(password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """
#     Verify a stored password against one provided by user
#     """
#     return pwd_context.verify(plain_password, hashed_password)
