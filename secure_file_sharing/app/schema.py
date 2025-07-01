from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class FileOut(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    email: EmailStr
    role: str
    user_id: int

class DownloadLinkResponse(BaseModel):
    download_link: str
    message: str = "success"