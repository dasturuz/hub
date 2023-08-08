from pydantic import BaseModel
from typing import Optional, List
from pydantic.datetime_parse import time,datetime,date


class Kurs_sanalariBase(BaseModel):
    fan_id: int
    teacher_id: int
    xona_id: int
    soat:str
    oquvchi_id: int
    bor_yoq: bool
    boshi: date
    oxiri:date



class Kurs_sanalariCreate(Kurs_sanalariBase):
    pass


class Kurs_sanalariUpdate(Kurs_sanalariBase):
    id: int


