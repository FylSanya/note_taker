from typing import Optional, List

from datetime import datetime

from app.schemas.base import BaseDBModel
from app.utils.object_id import OID


class ChecklistItem(BaseDBModel):
    text: str
    is_checked: bool


class TextField(BaseDBModel):
    text: str


class Note(BaseDBModel):
    id: Optional[OID]
    title: TextField
    text: TextField
    datetime: Optional[datetime]  # TODO: delete this field from necessary
    tags: List[Optional[str]] = None
    checklist_items: List[Optional[ChecklistItem]]
    list_items: List[Optional[TextField]]
