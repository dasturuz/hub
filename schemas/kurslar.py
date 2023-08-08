from pydantic import BaseModel
from typing import Optional, List
from pydantic.datetime_parse import time,datetime


class KurslarBase(BaseModel):
    fan_id: int
    teacher_id: int
    soat:str
    kurs_muddati:str



class KurslarCreate(KurslarBase):
    pass


class KurslarUpdate(KurslarBase):
    id: int


