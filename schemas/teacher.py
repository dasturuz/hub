
from pydantic import BaseModel
from typing import Optional, List



class TeacherBase(BaseModel):
    ism: str
    familiya: str
    tel: str
    fan_id: int
    password: str



class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(TeacherBase):
    id: int



class UpdateTeacherBalance(BaseModel):
    id: int
    balance: float
    user_id: int

class UpdateTeacherSalary(BaseModel):
    id: int
    salary: float
    user_id: int
class UpdateTeacherSalaryBalance(BaseModel):
    id: int
    balance: int
    salary: int
    user_id: int

class Token(BaseModel):
    access_token = str
    token = str


class TokenData(BaseModel):
    id: Optional[str] = None

class TeacherCurrent(BaseModel):
    id:int
    ism: str
    tel: str
    user_id:int
    password:str
    familiya: str
    fan_id:int
    status: bool