import datetime
from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.database import DatabaseManager
from app.schemas import Note
from app.utils.object_id import OID
from app.utils.logging import logger


class MongoManager(DatabaseManager):
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str, name: str):
        logger.info("Connecting to MongoDB.")
        self.client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10)
        self.db = self.client.get_database(name=name)
        logger.info("Connected to MongoDB.")

    async def close_database_connection(self):
        logger.info("Closing connection with MongoDB.")
        self.client.close()
        logger.info("Closed connection with MongoDB.")

    async def get_notes(self) -> List[Note]:
        notes_list = []
        notes_q = self.db.notes.find()
        async for note in notes_q:
            notes_list.append(Note(**note, id=note["_id"]))
        return notes_list

    async def get_note(self, note_id: OID) -> Note:
        note_q = await self.db.notes.find_one({"_id": ObjectId(note_id)})
        if note_q:
            return Note(**note_q, id=note_q["_id"])

    async def delete_note(self, note_id: OID):
        await self.db.notes.delete_one({"_id": ObjectId(note_id)})

    async def update_note(self, note_id: OID, note: Note):
        await self.db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": note.dict(exclude={"id"})})

    async def add_note(self, note: Note):
        note_document = note.dict(exclude={"id", "datetime"})
        note_document["datetime"] = datetime.datetime.now()
        await self.db.notes.insert_one(note_document)
