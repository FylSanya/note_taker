from typing import List

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.database import DatabaseManager
from app.schemas import Note
from app.schemas.notes import NoteDB
from app.schemas.templates import Template, TemplateDB
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
        self.db.notes.create_index(
            [("title", pymongo.TEXT), ("body", pymongo.TEXT)],
            name="search_index",
            default_language="english",
        )

        logger.info("Connected to MongoDB.")

    async def close_database_connection(self) -> None:
        """
        This method disconnects us from MongoDB
        :return:
        """
        logger.info("Closing connection with MongoDB.")
        self.client.close()
        logger.info("Closed connection with MongoDB.")

    async def get_templates(self) -> List[TemplateDB]:
        """
        This method get all templates from database.
        :return:
        """
        template_list = []
        template_q = self.db.templates.find()
        async for template in template_q:
            print(template)
            template_list.append(TemplateDB(**template, template_id=template["_id"]))
        return template_list

    async def add_template(self, template: Template) -> str:
        """
        This method add template to database.
        :param template: template data
        :return:
        """
        template_document = template.dict()
        print(template_document)
        inserted_template = await self.db.templates.insert_one(template_document)
        return inserted_template.inserted_id

    async def get_template(self, template_id: OID) -> TemplateDB:
        """
        This method get one template from database.
        :param template_id: Template OID
        :return:
        """
        template_q = await self.db.templates.find_one({"_id": ObjectId(template_id)})
        if template_q:
            return TemplateDB(**template_q, template_id=template_q["_id"])

    async def delete_template(self, template_id: OID) -> None:
        """
        This method delete template from database.
        :param template_id: Template OID
        :return:
        """
        await self.db.templates.delete_one({"_id": ObjectId(template_id)})

    async def update_template(self, template_id: OID, template: TemplateDB):
        """
        This method update template.
        :param template_id: Template OID
        :param template: New data
        :return:
        """
        await self.db.templates.update_one(
            {"_id": ObjectId(template_id)},
            {"$set": template.dict(exclude={"template_id"})},
        )

    async def get_notes(self) -> List[NoteDB]:
        """
        This method get all notes from database.
        :return:
        """
        notes_list = []
        notes_q = self.db.notes.find()
        async for note in notes_q:
            print(note)
            notes_list.append(NoteDB(**note, note_id=note["_id"]))
        return notes_list

    async def get_filtered_notes(self, filter_query: str) -> List[NoteDB]:
        """
        This method get filtered notes from database.
        :return:
        """
        notes_list = []
        notes_q = self.db.notes.find(
            {
                "$text": {
                    "$search": filter_query,
                    "$caseSensitive": False,
                }
            }
        )
        async for note in notes_q:
            print(note)
            notes_list.append(NoteDB(**note, note_id=note["_id"]))
        return notes_list

    async def get_note(self, note_id: OID) -> NoteDB:
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

    async def update_note(self, note_id: OID, note: NoteDB):
        """
        This method update note.
        :param note_id: Note OID
        :param note: New data
        :return:
        """
        await self.db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": note.dict(exclude={"note_id"})})

    async def add_note(self, note: Note) -> str:
        """
        This method add note to database.
        :param note: Note data
        :return:
        """
        note_document = note.dict()
        print(note_document)
        inserted_note = await self.db.notes.insert_one(note_document)
        return inserted_note.inserted_id
