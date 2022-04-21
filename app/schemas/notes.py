from typing import Optional, List

from datetime import datetime

from pydantic import BaseModel

from app.utils.object_id import OID


class ChecklistItem(BaseModel):
    """
    This is class to Checklist Item
    """

    text: str
    is_checked: bool


class TextField(BaseModel):
    """
    This is class fot text field
    """

    text: str


class Note(BaseModel):
    """
    This is class for note
    """

    id: Optional[OID]
    title: TextField
    text: TextField
    datetime: Optional[datetime]  # TODO: delete this field from necessary
    tags: List[Optional[str]] = None
    checklist_items: List[Optional[ChecklistItem]]
    list_items: List[Optional[TextField]]
