from typing import List

from fastapi import Depends
from starlette import status
from starlette.responses import Response

from app.database.mongo_manager import MongoManager
from app.schemas import Note
from app.schemas.notes import NoteDB
from app.utils.logging import logger
from app.utils.object_id import OID
from app.database import get_database
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter()


@cbv(router)
class NoteAPI:
    db: MongoManager = Depends(get_database)

    @router.get("/")
    async def all_notes(self) -> List[NoteDB]:
        """
        This route method call db's get_notes method and return it.
        :return:
        """
        return await self.db.get_notes()

    @router.get("/search/{filter_query}/")
    async def filtered_notes(self, filter_query: str | None) -> List[NoteDB]:
        """
        This route method call db's get_notes method and return it.
        :param filter_query:
        :return:
        """
        return await self.db.get_filtered_notes(filter_query)

    @router.get("/{note_id}")
    async def one_note(self, note_id: OID) -> NoteDB | None:
        """
        This route method call db's get_note method and return it.
        :param note_id: Note OID
        :return:
        """
        return await self.db.get_note(note_id=note_id)

    @router.put("/{note_id}")
    async def update_note(self, note_id: OID, note: Note):
        """
        This route method call db's update_note method and return it.
        :param note_id: Note OID
        :param note: Note
        :return:
        """

        matched_count = await self.db.update_note(note=note, note_id=note_id)
        if matched_count == 0:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return_result = NoteDB(**note.dict(), note_id=note_id)
        return return_result

    @router.post("/", status_code=201)
    async def add_note(self, note_response: Note) -> str:
        """
        This route method call db's add_note method and return it.
        :param note_response: Note
        :return:
        """
        return await self.db.add_note(note_response)

    @router.delete("/{note_id}")
    async def delete_note(self, note_id: OID):
        """
        This route method call db's delete_note method and return it.
        :param note_id: Note OID
        :return:
        """
        _ = await self.db.delete_note(note_id=note_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
