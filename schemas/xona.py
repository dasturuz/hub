from pydantic import BaseModel
from typing import Optional, List



class XonaBase(BaseModel):
    xona_nomi: str
    raqami: int



class XonaCreate(XonaBase):
    pass


class XonaUpdate(XonaBase):
    id: int
