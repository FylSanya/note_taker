from app.database.mongo_manager import MongoManager

db = MongoManager()


async def get_database() -> MongoManager:
    return db
