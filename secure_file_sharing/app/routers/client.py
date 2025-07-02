from fastapi import APIRouter, HTTPException
from ..schema import UserCreate, UserInDB
from ..database import db
from ..auth import hash_password

router = APIRouter()

@router.post("/signup")
async def signup(user: UserCreate):
    existing = await db["users"].find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email exists")
    user_dict = user.dict()
    user_dict["role"] = "client"
    user_dict["is_verified"] = False
    user_dict["password"] = hash_password(user_dict["password"])
    result = await db["users"].insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return user_dict

@router.get("/users")
async def list_users():
    users = []
    async for user in db["users"].find({}):
        user["id"] = str(user["_id"])
        users.append(user)
    return users