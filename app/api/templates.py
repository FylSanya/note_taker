from typing import List

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from app.schemas.templates import Template, TemplateDB
from app.utils.object_id import OID
from app.database import DatabaseManager, get_database


router = APIRouter()


@router.get("/")
async def all_templates(
    db: DatabaseManager = Depends(get_database),
) -> List[TemplateDB]:
    """
    This route method call db's get_notes method and return it.
    :param db: DB manager
    :return:
    """
    templates = await db.get_templates()
    return templates


@router.get("/{template_id}")
async def one_template(template_id: OID, db: DatabaseManager = Depends(get_database)) -> TemplateDB:
    """
    This route method call db's get_template method and return it.
    :param template_id: template OID
    :param db: DB manager
    :return:
    """
    template = await db.get_template(template_id=template_id)
    return template


@router.post("/", status_code=201)
async def add_template(template_response: Template, db: DatabaseManager = Depends(get_database)) -> str:
    """
    This route method call db's add_template method and return it.
    :param template_response: template
    :param db: DB manager
    :return:
    """
    inserted_template_id = await db.add_template(template_response)
    return str(inserted_template_id)


@router.delete("/{template_id}")
async def delete_template(template_id: OID, db: DatabaseManager = Depends(get_database)) -> JSONResponse:
    """
    This route method call db's delete_template method and return it.
    :param template_id: template OID
    :param db: DB manager
    :return:
    """
    await db.delete_template(template_id=template_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{template_id}")
async def update_template(
    template_id: OID, template: TemplateDB, db: DatabaseManager = Depends(get_database)
) -> TemplateDB:
    """
    This route method call db's update_template method and return it.
    :param template_id: template OID
    :param template: template
    :param db: DB manager
    :return:
    """
    template = await db.update_template(template=template, template_id=template_id)
    return template
