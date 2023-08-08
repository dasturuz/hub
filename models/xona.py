from sqlalchemy import Column, Integer, String, Boolean,Float,Text,ForeignKey,DateTime,func

from sqlalchemy.orm import *

from db import Base

class Xona(Base):
    __tablename__ = "Xona"
    id = Column(Integer, primary_key=True)
    xona_nomi = Column(String,nullable=False)
    raqami = Column(Integer,nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, nullable=False)

    kurs_sanalari3 = relationship('Kurs_sanalari', back_populates='xona_id1')