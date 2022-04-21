from typing import Optional, List

from datetime import datetime

from pydantic import BaseModel

from app.utils.object_id import OID


class Note(BaseModel):
    """
    This is class for note
    """

    title: str
    body: str
    created: Optional[datetime]
    modified: Optional[datetime]


class NoteDB(Note):
    """
    This is class for note in database
    """

    note_id: Optional[OID]
