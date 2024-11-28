from fastapi import Response
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# Configuration for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()
# JWT secret key (should ideally come from environment variable)
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # default to 15 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_access_token_cookie(response: Response, data: dict, expires_delta: timedelta = None):
    token = create_access_token(data, expires_delta)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,  # HTTP-only, not accessible via JavaScript
        max_age=expires_delta.total_seconds() if expires_delta else 15 * 60,  # seconds
        expires=expires_delta.total_seconds() if expires_delta else 15 * 60,
        path="/",
        secure=True,  # Use with HTTPS
        samesite="Lax"  # Helps mitigate CSRF attacks
    )
    return token

def remove_access_token_cookie(response: Response):
    response.delete_cookie("access_token", path="/")