from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from ..database.connection import get_db
from ..models import Users as UserModel
from ..schemas.users import UserSignupRequest, UserLoginRequest
from ..utils import hash_password, verify_password, create_access_token_cookie, remove_access_token_cookie
from datetime import datetime, timedelta

user_router = APIRouter(prefix='/user', tags=["User"])

@user_router.post("/signup")
async def signup(user: UserSignupRequest, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.user_id == user.user_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    hashed_password = hash_password(user.password)
    new_user = UserModel(user_id=user.user_id, password=hashed_password, nickname=user.nickname)
    db.add(new_user)
    db.commit()
    return {"message": "User successfully registered"}

@user_router.post("/login")
async def login(form_data: UserLoginRequest, db: Session = Depends(get_db), response: Response = None):
    user = db.query(UserModel).filter(UserModel.user_id == form_data.user_id).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    expires_delta = timedelta(days=1)  # 1 day token expiration
    token = create_access_token_cookie(response, {"sub": user.user_id}, expires_delta)
    return {"access_token": token}

@user_router.post("/logout")
async def logout(response: Response):
    remove_access_token_cookie(response)
    return {"message": "Logged out successfully"}
