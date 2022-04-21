import datetime
from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.database import DatabaseManager
from app.schemas import Note
from app.schemas.notes import NoteDB
from app.utils.object_id import OID
from app.utils.logging import logger


class MongoManager(DatabaseManager):
    """
    This class in manager for MongoDB.
    """

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str, name: str) -> None:
        """
        This method connects us to MongoDB
        :param path: Path to Mongo
        :param name: Name of DB
        :return:
        """
        logger.info("Connecting to MongoDB.")
        self.client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10)
        self.db = self.client.get_database(name=name)
        logger.info("Connected to MongoDB.")

    async def close_database_connection(self) -> None:
        """
        This method disconnects us from MongoDB
        :return:
        """
        logger.info("Closing connection with MongoDB.")
        self.client.close()
        logger.info("Closed connection with MongoDB.")

    async def get_notes(self) -> List[Note]:
        """
        This method get all notes from database.
        :return:
        """
        notes_list = []
        notes_q = self.db.notes.find()
        async for note in notes_q:
            print(note)
            # del note['note_id']
            notes_list.append(NoteDB(**note, note_id=note["_id"]))
        return notes_list

    async def get_note(self, note_id: OID) -> Note:
        """
        This method get one note from database.
        :param note_id: Note OID
        :return:
        """
        note_q = await self.db.notes.find_one({"_id": ObjectId(note_id)})
        if note_q:
            return NoteDB(**note_q, note_id=note_q["_id"])

    async def delete_note(self, note_id: OID) -> None:
        """
        This method delete note from database.
        :param note_id: Note OID
        :return:
        """
        await self.db.notes.delete_one({"_id": ObjectId(note_id)})

    async def update_note(self, note_id: OID, note: Note):
        """
        This method update note.
        :param note_id: Note OID
        :param note: New data
        :return:
        """
        await self.db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": note.dict(exclude={"note_id"})})

    async def add_note(self, note: Note) -> None:
        """
        This method add note to database.
        :param note: Note data
        :return:
        """
        note_document = note.dict()
        print(note_document)
        inserted_note = await self.db.notes.insert_one(note_document)
        return inserted_note.inserted_id
