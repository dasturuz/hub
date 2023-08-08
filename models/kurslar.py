from sqlalchemy import Column, Integer, String, Boolean,Float,Text,ForeignKey,DateTime,func

from sqlalchemy.orm import *

from db import Base

class Kurslar(Base):
    __tablename__ = "Kurslar"
    id = Column(Integer, primary_key=True)
    fan_id = Column(Integer, ForeignKey("Fan.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("Teacher.id"),nullable=False)
    soat = Column(String(50), nullable=False)
    kurs_muddati = Column(String(20),nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, nullable=False)

    fan_id2 = relationship('Fan',back_populates='kurs_id1')
    teacher_id2 = relationship('Teacher',back_populates='kurs_id2')