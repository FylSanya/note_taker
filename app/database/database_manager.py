from abc import abstractmethod
from typing import List

from app.schemas import Note
from app.utils.object_id import OID


class DatabaseManager:
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
    async def get_notes(self) -> List[Note]:
        pass

    @abstractmethod
    async def get_note(self, note_id: OID) -> Note:
        pass

    @abstractmethod
    async def add_note(self, note: Note):
        pass

    @abstractmethod
    async def update_note(self, note_id: OID, note: Note):
        pass

    @abstractmethod
    async def delete_note(self, note_id: OID):
        pass
