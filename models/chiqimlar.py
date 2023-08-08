from sqlalchemy import Column, Integer, String, Boolean,Float,Text,ForeignKey,DateTime,func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import *

from db import Base

class Chiqimlar(Base):
    __tablename__ = "Chiqimlar"
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("Teacher.id"), nullable=False)
    money = Column(Integer,nullable=False)
    comment = Column(String,nullable=False)
    type = Column(String, nullable=False)
    currency = Column(String(),nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, nullable=False)

    teacher_id4 = relationship('Teacher',back_populates='chiqimlar_id1')
