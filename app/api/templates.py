from typing import List

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status
from starlette.responses import Response

from app.database.mongo_manager import MongoManager
from app.schemas.templates import Template, TemplateDB
from app.utils.object_id import OID
from app.database import get_database

router = InferringRouter()


@cbv(router)
class TemplateAPI:
    db: MongoManager = Depends(get_database)

    @router.get("/")
    async def all_templates(self) -> List[TemplateDB]:
        """
        This route method call db's get_notes method and return it.
        :return:
        """
        return await self.db.get_templates()

    @router.get("/{template_id}")
    async def one_template(self, template_id: OID) -> TemplateDB | None:
        """
        This route method call db's get_template method and return it.
        :param template_id: template OID
        :return:
        """
        return await self.db.get_template(template_id=template_id)

    @router.post("/", status_code=201)
    async def add_template(self, template_response: Template) -> str:
        """
        This route method call db's add_template method and return it.
        :param template_response: template
        :return:
        """
        return await self.db.add_template(template_response)

    @router.delete("/{template_id}")
    async def delete_template(self, template_id: OID):
        """
        This route method call db's delete_template method and return it.
        :param template_id: template OID
        :return: JSONResponse
        """
        _ = await self.db.delete_template(template_id=template_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.put("/{template_id}")
    async def update_template(self, template_id: OID, template: Template):
        """
        This route method call db's update_template method and return it.
        :param template_id: template OID
        :param template: template
        :return:
        """
        matched_count = await self.db.update_template(template=template, template_id=template_id)
        if matched_count == 0:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return_result = TemplateDB(**template.dict(), note_id=template_id)
        return return_result
