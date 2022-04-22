from typing import List

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from app.schemas import Note
from app.schemas.notes import NoteDB
from app.utils.object_id import OID
from app.database import DatabaseManager, get_database

router = APIRouter()


@router.get("/")
async def all_notes(db: DatabaseManager = Depends(get_database)) -> List[NoteDB]:
    """
    This route method call db's get_notes method and return it.
    :param db: DB manager
    :return:
    """
    notes = await db.get_notes()
    return notes


@router.get("/{filter_query}")
async def filtered_notes(filter_query: str, db: DatabaseManager = Depends(get_database)) -> List[NoteDB]:
    """
    This route method call db's get_notes method and return it.
    :param filter_query:
    :param db: DB manager
    :return:
    """
    notes = await db.get_filtered_notes(filter_query)
    return notes


@router.get("/{note_id}")
async def one_note(note_id: OID, db: DatabaseManager = Depends(get_database)) -> NoteDB:
    """
    This route method call db's get_note method and return it.
    :param note_id: Note OID
    :param db: DB manager
    :return:
    """
    note = await db.get_note(note_id=note_id)
    return note


@router.put("/{note_id}")
async def update_note(note_id: OID, note: Note, db: DatabaseManager = Depends(get_database)) -> NoteDB:
    """
    This route method call db's update_note method and return it.
    :param note_id: Note OID
    :param note: Note
    :param db: DB manager
    :return:
    """
    note = await db.update_note(note=note, note_id=note_id)
    return note


@router.post("/", status_code=201)
async def add_note(note_response: Note, db: DatabaseManager = Depends(get_database)) -> str:
    """
    This route method call db's add_note method and return it.
    :param note_response: Note
    :param db: DB manager
    :return:
    """
    inserted_note_id = await db.add_note(note_response)
    return str(inserted_note_id)


@router.delete("/{note_id}")
async def delete_note(note_id: OID, db: DatabaseManager = Depends(get_database)) -> JSONResponse:
    """
    This route method call db's delete_note method and return it.
    :param note_id: Note OID
    :param db: DB manager
    :return:
    """
    await db.delete_note(note_id=note_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
