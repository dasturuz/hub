from pydantic import BaseModel
from typing import Optional, List



class FanBase(BaseModel):
    nomi:str



class FanCreate(FanBase):
    pass


class FanUpdate(FanBase):
    id: int


