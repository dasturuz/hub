
import datetime
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
from pydantic.datetime_parse import date
from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.teacher import teacher_current
from functions.kurs_sanalari import one_kurs_sanalari, all_kurs_sanalari, update_kurs_sanalari, add_kurs_sanalari, delete_kurs_sanalari
from schemas.kurs_sanalari import Kurs_sanalariBase,Kurs_sanalariCreate,Kurs_sanalariUpdate
from schemas.teacher import TeacherCurrent
router_kurs_sanalari = APIRouter()



@router_kurs_sanalari.post("/add")
def kurs_sanalari_qoshish(form:Kurs_sanalariCreate,db:Session=Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user)):
    return add_kurs_sanalari(form=form,user=current_user,db=db)


@router_kurs_sanalari.get('/',  status_code = 200)
def get_kurs_sanalari(search:str=None,status:bool=True,id:int=0,start_date:date=datetime.datetime.now().date().min,end_date:date=datetime.datetime.now().date(),page:int=1,limit:int=2, db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_kurs_sanalari(id, db)
    else :
        return all_kurs_sanalari(search=search,status=status,start_date=start_date,end_date=end_date,page=page,limit=limit,db=db)




@router_kurs_sanalari.put("/update")
def kurs_sanalari_update(form: Kurs_sanalariUpdate, db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user)) :
    if update_kurs_sanalari(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_kurs_sanalari.delete('/{id}',  status_code = 200)
def kurs_sanalari_delete(id: int = 0,db: Session = Depends(get_db), current_user: TeacherCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id:
        return delete_kurs_sanalari(id, db)