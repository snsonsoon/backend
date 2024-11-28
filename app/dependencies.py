from fastapi import Depends, HTTPException, Security
import jwt
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

# OAuth2PasswordBearer is a class that we instantiate to get a token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Assuming you have a secret key for JWT and it is stored securely
SECRET_KEY = os.environ.get('SECRET_KEY')

# JWT identity extraction
def get_jwt_identity(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")  # 'sub' is typically used for the user ID in JWT
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

