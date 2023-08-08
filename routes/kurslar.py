
import datetime
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
from pydantic.datetime_parse import date
from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.teacher import teacher_current
from functions.kurslar import one_kurslar, all_kurslar, update_kurslar, add_kurslar, delete_kurslar
from schemas.kurslar import KurslarBase,KurslarCreate,KurslarUpdate
from schemas.teacher import TeacherCurrent
router_kurslar = APIRouter()



@router_kurslar.post("/add")
def kurslar_qoshish(form:KurslarCreate,db:Session=Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user)):
    return add_kurslar(form=form,user=current_user,db=db)


@router_kurslar.get('/',  status_code = 200)
def get_kurslar(search:str=None,status:bool=True,id:int=0,start_date:date=datetime.datetime.now().date().min,end_date:date=datetime.datetime.now().date(),page:int=1,limit:int=2, db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_kurslar(id, db)
    else :
        return all_kurslar(search=search,status=status,start_date=start_date,end_date=end_date,page=page,limit=limit,db=db)




@router_kurslar.put("/update")
def kurslar_update(form: KurslarUpdate, db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user)) :
    if update_kurslar(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_kurslar.delete('/{id}',  status_code = 200)
def kurslar_delete(id: int = 0,db: Session = Depends(get_db), current_user: TeacherCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id:
        return delete_kurslar(id, db)