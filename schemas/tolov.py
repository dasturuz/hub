from pydantic import BaseModel
from typing import Optional, List
from pydantic.datetime_parse import date


class TolovBase(BaseModel):
    fan_id: int
    oquvchi_id: int
    oy: date
    price: int
    type: str

class TolovCreate(TolovBase):
    pass


class TolovUpdate(TolovBase):
    id: int

