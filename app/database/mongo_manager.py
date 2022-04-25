from typing import List, Optional, Tuple

import pymongo
from bson import ObjectId
from motor import MotorCollection
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.results import DeleteResult

from app.schemas import Note
from app.schemas.notes import NoteDB
from app.schemas.templates import Template, TemplateDB
from app.utils.object_id import OID
from app.utils.logging import logger


class MongoManager:
    """
    This class in manager for MongoDB.
    """

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None
    note_collection: MotorCollection = None
    template_collection: MotorCollection = None
    notes_collection_name: str = "notes"
    templates_collection_name: str = "templates"

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
        self.note_collection = self.db.get_collection(self.notes_collection_name)
        self.template_collection = self.db.get_collection(self.templates_collection_name)
        logger.info("Connected to MongoDB.")

    async def close_database_connection(self) -> None:
        """
        This method disconnects us from MongoDB
        :return:
        """
        logger.info("Closing connection with MongoDB.")
        self.client.close()
        logger.info("Closed connection with MongoDB.")

    async def get_notes(self) -> List[NoteDB]:
        """
        This method get all notes from database.
        :return:
        """
        notes_list = []
        notes_q = self.note_collection.find()

        async for note in notes_q:
            notes_list.append(NoteDB(**note, note_id=note["_id"]))
        return notes_list
        # we can't do this because of AsyncIOMotorCursor object is not iterable
        # return [NoteDB(**note, note_id=note["_id"]) for note in notes_q]

    async def get_filtered_notes(self, filter_query: str) -> List[NoteDB]:
        """
        This method get filtered notes from database.
        :return:
        """
        notes_list = []
        notes_q = self.note_collection.find(
            {
                "$text": {
                    "$search": filter_query,
                    "$caseSensitive": False,
                }
            }
        )
        async for note in notes_q:
            notes_list.append(NoteDB(**note, note_id=note["_id"]))
        return notes_list

    async def get_note(self, note_id: OID) -> NoteDB | None:
        """
        This method get one note from database.
        :param note_id: Note OID
        :return:
        """
        note_q = await self.note_collection.find_one({"_id": ObjectId(note_id)})
        if note_q:
            return NoteDB(**note_q, note_id=note_q["_id"])
        return None

    async def delete_note(self, note_id: OID) -> DeleteResult:
        """
        This method delete note from database.
        :param note_id: Note OID
        :return:
        """
        return await self.note_collection.delete_one({"_id": ObjectId(note_id)})

    async def update_note(self, note_id: OID, note: Note) -> int:
        """
        This method update note.
        :param note_id: Note OID
        :param note: New data
        :return:
        """
        result = await self.note_collection.update_one(
            {"_id": ObjectId(note_id)}, {"$set": note.dict(exclude={"note_id"})}
        )

        return result.matched_count

    async def add_note(self, note: Note) -> str:
        """
        This method add note to database.
        :param note: Note data
        :return:
        """
        note_document = note.dict()
        inserted_note = await self.note_collection.insert_one(note_document)

        return str(inserted_note.inserted_id)

    async def get_templates(self) -> List[TemplateDB]:
        """
        This method get all templates from database.
        :return:
        """
        template_list = []
        template_q = self.template_collection.find()
        async for template in template_q:
            template_list.append(TemplateDB(**template, template_id=template["_id"]))
        return template_list

    async def add_template(self, template: Template) -> str:
        """
        This method add template to database.
        :param template: template data
        :return:
        """
        template_document = template.dict()
        inserted_template = await self.template_collection.insert_one(template_document)
        return str(inserted_template.inserted_id)

    async def get_template(self, template_id: OID) -> TemplateDB | None:
        """
        This method get one template from database.
        :param template_id: Template OID
        :return:
        """
        template_q = await self.template_collection.find_one({"_id": ObjectId(template_id)})
        if template_q:
            return TemplateDB(**template_q, template_id=template_q["_id"])
        return None

    async def delete_template(self, template_id: OID) -> DeleteResult:
        """
        This method delete template from database.
        :param template_id: Template OID
        :return:
        """
        return await self.template_collection.delete_one({"_id": ObjectId(template_id)})

    async def update_template(self, template_id: OID, template: Template) -> int:
        """
        This method update template.
        :param template_id: Template OID
        :param template: New data
        :return:
        """
        result = await self.template_collection.update_one(
            {"_id": ObjectId(template_id)},
            {"$set": template.dict(exclude={"template_id"})},
        )

        return result.matched_count
