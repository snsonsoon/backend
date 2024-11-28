from pydantic import BaseModel

class UserSignupRequest(BaseModel):
    user_id: str
    password: str
    nickname: str

class UserLoginRequest(BaseModel):
    user_id: str
    password: str