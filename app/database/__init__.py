from app.database.database_manager import DatabaseManager
from app.database.mongo_manager import MongoManager

db = MongoManager()


async def get_database() -> DatabaseManager:
    return db
