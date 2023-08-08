from sqlalchemy import Column, Integer, String, Boolean,Float,Text,ForeignKey,DateTime,func,Time

from sqlalchemy.orm import *

from db import Base

class Oquvchi(Base):
    __tablename__ = "Oquvchi"
    id = Column(Integer, primary_key=True)
    ism = Column(String(30), nullable=False)
    familiya = Column(String(30), nullable=False)
    tel = Column(String(50), nullable=False)
    yosh = Column(Integer,nullable=False)
    address = Column(String, nullable=True)
    fan_id = Column(Integer, ForeignKey("Fan.id"),nullable=False)

    soat = Column(String(50),nullable=False)
    date =  Column(DateTime(timezone=True),default=func.now(),nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, nullable=False)

    tolov_id1 = relationship('Tolov', back_populates='oquvchi_id1')

    kurs_sanalari4 = relationship('Kurs_sanalari', back_populates='oquvchi_id2')

    subject = relationship('Fan',back_populates='student')