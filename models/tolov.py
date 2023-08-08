from sqlalchemy import Column, Integer, String, Boolean,Float,Text,ForeignKey,DateTime,func,Date

from sqlalchemy.orm import *

from db import Base

class Tolov(Base):
    __tablename__ = "Tolov"
    id = Column(Integer, primary_key=True)
    fan_id = Column(Integer, ForeignKey("Fan.id"), nullable=False)
    oquvchi_id = Column(Integer, ForeignKey("Oquvchi.id"), nullable=False)
    oy = Column(Date(),nullable=False)
    price = Column(Integer,nullable=False)
    type = Column(String,nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, nullable=False)

    tekshirish = relationship('Fan',back_populates='mablag')
    oquvchi_id1 = relationship('Oquvchi',back_populates='tolov_id1')
