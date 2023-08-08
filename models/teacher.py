from sqlalchemy import Column, Integer, String, Boolean,Float,Text,ForeignKey,DateTime,func

from sqlalchemy.orm import *

from db import Base


class Teacher(Base):
    __tablename__ = "Teacher"
    id =Column(Integer,primary_key=True, nullable=False)
    ism = Column(String(30),nullable=False)
    familiya = Column(String(30),nullable=False)
    tel = Column(String(40),unique=True,nullable=False)
    fan_id = Column(Integer, ForeignKey("Fan.id"), nullable=False)
    user_id = Column(Integer,nullable=False)
    password = Column(String(200), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    date = Column(DateTime(timezone=True),default=func.now(),nullable=False)
    token = Column(String(400), default='', nullable=True)















    fan_id1 = relationship('Fan',back_populates='teacher_id1')

    kurs_id2 = relationship('Kurslar', back_populates='teacher_id2')

    kurs_sanalari2 = relationship('Kurs_sanalari', back_populates='teacher_id3')

    chiqimlar_id1 = relationship('Chiqimlar', back_populates='teacher_id4')

