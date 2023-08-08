
import datetime
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
from pydantic.datetime_parse import date
from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.teacher import teacher_current
from functions.chiqimlar import one_chiqimlar, all_chiqimlar, update_chiqimlar, add_chiqimlar, delete_chiqimlar
from schemas.chiqimlar import ChiqimlarBase,ChiqimlarCreate,ChiqimlarUpdate
from schemas.teacher import TeacherCurrent
router_chiqimlar = APIRouter()



@router_chiqimlar.post("/add")
def chiqimlar_qoshish(form:ChiqimlarCreate,db:Session=Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user)):
    return add_chiqimlar(form=form,user=current_user,db=db)


@router_chiqimlar.get('/',  status_code = 200)
def get_chiqimlar(search:str=None,status:bool=True,id:int=0,start_date:date=datetime.datetime.now().date().min,end_date:date=datetime.datetime.now().date(),page:int=1,limit:int=2, db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_chiqimlar(id, db)
    else :
        return all_chiqimlar(search=search,status=status,start_date=start_date,end_date=end_date,page=page,limit=limit,db=db)




@router_chiqimlar.put("/update")
def chiqimlar_update(form: ChiqimlarUpdate, db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user)) :
    if update_chiqimlar(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_chiqimlar.delete('/{id}',  status_code = 200)
def chiqimlar_delete(id: int = 0,db: Session = Depends(get_db), current_user: TeacherCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id:
        return delete_chiqimlar(id, db)