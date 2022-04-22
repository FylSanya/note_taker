from typing import Optional

from pydantic import BaseModel

from app.utils.object_id import OID


class Template(BaseModel):
    """
    This is class for note template
    """

    title: str
    body: str


class TemplateDB(Template):
    """
    This is class for note in database
    """

    template_id: Optional[OID]
