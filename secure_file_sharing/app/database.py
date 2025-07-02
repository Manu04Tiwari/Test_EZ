from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGODB_URL, DB_NAME

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]