from pydantic import BaseModel
from typing import Optional, List
from pydantic.datetime_parse import time,datetime,date


class OquvchiBase(BaseModel):
    ism:str
    familiya:str
    tel:str
    yosh:int
    address:str
    soat:str
    fan_id:int

class OquvchiCreate(OquvchiBase):
    pass

class OquvchiUpdate(OquvchiBase):
    id: int


