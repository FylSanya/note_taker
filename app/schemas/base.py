from pydantic import BaseModel


class BaseDBModel(BaseModel):
    pass
    # class Config:
    #     orm_mode = True
    #     allow_population_by_field_name = True
    #
    #     @classmethod
    #     def alias_generator(cls, string: str) -> str:
    #         """Camel case generator"""
    #         temp = string.split('_')
    #         return temp[0] + ''.join(ele.title() for ele in temp[1:])
