from fastapi import APIRouter, Depends

from app.schemas import Note
from app.utils.object_id import OID
from app.database import DatabaseManager, get_database

router = APIRouter()


@router.get("/")
async def all_notes(db: DatabaseManager = Depends(get_database)):
    notes = await db.get_notes()
    return notes


@router.get("/{note_id}")
async def one_note(note_id: OID, db: DatabaseManager = Depends(get_database)):
    note = await db.get_note(note_id=note_id)
    return note


@router.put("/{note_id}")
async def update_note(note_id: OID, note: Note, db: DatabaseManager = Depends(get_database)):
    note = await db.update_note(note=note, note_id=note_id)
    return note


@router.post("/", status_code=201)
async def add_note(note_response: Note, db: DatabaseManager = Depends(get_database)):
    note = await db.add_note(note_response)
    return note


@router.delete("/{note_id}")
async def delete_note(note_id: OID, db: DatabaseManager = Depends(get_database)):
    await db.delete_note(note_id=note_id)
