from sqlalchemy import Column, Integer, String, Boolean,Float,Text,ForeignKey,DateTime,func

from sqlalchemy.orm import *

from db import Base

class Fan(Base):
    __tablename__ = "Fan"
    id = Column(Integer, primary_key=True)
    nomi = Column(String,nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, nullable=False)

    mablag = relationship('Tolov', back_populates='tekshirish')

    teacher_id1 = relationship('Teacher', back_populates='fan_id1')

    kurs_id1 = relationship('Kurslar',back_populates='fan_id2')

    kurs_sanalari1 = relationship('Kurs_sanalari', back_populates='fan_id3')

    student = relationship('Oquvchi', back_populates='subject')