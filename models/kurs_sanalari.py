from sqlalchemy import Column, Integer, String, Boolean,Float,Text,ForeignKey,DateTime,func,Date

from sqlalchemy.orm import *

from db import Base

class Kurs_sanalari(Base):
    __tablename__ = "Kurs_sanalari"
    id = Column(Integer, primary_key=True)
    fan_id = Column(Integer, ForeignKey("Fan.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("Teacher.id"), nullable=False)
    xona_id = Column(Integer,ForeignKey("Xona.id"),nullable=False)
    soat = Column(String(50), nullable=False)
    oquvchi_id = Column(Integer, ForeignKey("Oquvchi.id"),nullable=False)
    bor_yoq = Column(Boolean,nullable=False)
    boshi = Column(Date,nullable=False)
    oxiri = Column(Date,nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, nullable=False)

    fan_id3 = relationship('Fan',back_populates='kurs_sanalari1')

    teacher_id3 = relationship('Teacher',back_populates='kurs_sanalari2')

    xona_id1 = relationship('Xona',back_populates='kurs_sanalari3')

    oquvchi_id2 = relationship('Oquvchi',back_populates='kurs_sanalari4')