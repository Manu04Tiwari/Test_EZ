from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserInDB(UserCreate):
    id: Optional[str]
    role: str
    is_verified: bool = False

class FileOut(BaseModel):
    id: str
    filename: str
    uploaded_at: datetime
    uploaded_by: str