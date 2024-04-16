from bson import ObjectId
from pydantic.json import ENCODERS_BY_TYPE


class PydanticObjectId(ObjectId):
    """
    Object Id field. Compatible with Pydantic.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate
   
    #The validator is doing nothing
    @classmethod
    def validate(cls, v):
        return PydanticObjectId(v)

    #Here you modify the schema to tell it that it will work as an string
    @classmethod
    def __modify_schema__(cls, field_schema: dict):
        field_schema.update(
            type="string",
            examples=["5eb7cf5a86d9755df3a6c593", "5eb7cfb05e32e07750a1756a"],
        )

#Here you encode the ObjectId as a string
ENCODERS_BY_TYPE[PydanticObjectId] = str