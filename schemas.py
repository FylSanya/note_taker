from typing import List, Optional

from pydantic import BaseModel
from datetime import date


class Checklist(BaseModel):
    text: str
    status: bool


class TextField(BaseModel):
    text: str


class Note(BaseModel):
    title: TextField
    text: TextField
    date: date
    tags: List[Optional[str]] = None
    checklist_items: List[Optional[Checklist]]
    list_items: List[Optional[TextField]]
