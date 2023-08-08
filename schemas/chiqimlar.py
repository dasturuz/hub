from pydantic import BaseModel
from typing import Optional, List



class ChiqimlarBase(BaseModel):
    teacher_id: int
    money: int
    comment:str
    type:str
    currency:str


class ChiqimlarCreate(ChiqimlarBase):
    pass


class ChiqimlarUpdate(ChiqimlarBase):
    id: int


