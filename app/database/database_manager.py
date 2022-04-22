from abc import abstractmethod
from typing import List

from app.schemas import Note
from app.schemas.notes import NoteDB
from app.schemas.templates import TemplateDB, Template
from app.utils.object_id import OID


class DatabaseManager:
    """
    This class is our abstract DB manager.
    """

    @property
    def client(self):
        raise NotImplementedError

    @property
    def db(self):
        raise NotImplementedError

    @abstractmethod
    async def connect_to_database(self, path: str, name: str):
        pass

    @abstractmethod
    async def close_database_connection(self):
        pass

    @abstractmethod
    async def get_notes(self) -> List[NoteDB]:
        pass

    @abstractmethod
    async def get_note(self, note_id: OID) -> NoteDB:
        pass

    @abstractmethod
    async def add_note(self, note: Note):
        pass

    @abstractmethod
    async def update_note(self, note_id: OID, note: NoteDB):
        pass

    @abstractmethod
    async def delete_note(self, note_id: OID):
        pass

    @abstractmethod
    async def get_templates(self) -> List[TemplateDB]:
        pass

    @abstractmethod
    async def get_template(self, template_id: OID) -> TemplateDB:
        pass

    @abstractmethod
    async def add_template(self, template: Template):
        pass

    @abstractmethod
    async def delete_template(self, template_id: OID):
        pass

    @abstractmethod
    async def update_template(self, template_id: OID, template: TemplateDB):
        pass

    @abstractmethod
    def get_filtered_notes(self, filter_query):
        pass
