

import datetime
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
from pydantic.datetime_parse import date
from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.teacher import teacher_current
from functions.oquvchi import one_oquvchi, all_oquvchi, update_oquvchi, add_oquvchi, delete_oquvchi
from schemas.oquvchi import OquvchiBase,OquvchiCreate,OquvchiUpdate
from schemas.teacher import TeacherCurrent
router_oquvchi = APIRouter()



@router_oquvchi.post("/add")
def oquvchi_qoshish(form:OquvchiCreate,db:Session=Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user)):
    return add_oquvchi(form=form,user=current_user,db=db)


@router_oquvchi.get('/',  status_code = 200)
def get_tolov(search:str=None,status:bool=True,id:int=0,start_date:date=datetime.datetime.now().date().min,end_date:date=datetime.datetime.now().date(),page:int=1,limit:int=2, db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_oquvchi(id, db)
    else :
        return all_oquvchi(search=search,status=status,start_date=start_date,end_date=end_date,page=page,limit=limit,db=db)




@router_oquvchi.put("/update")
def oquvchi_update(form: OquvchiUpdate, db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user)) :
    if update_oquvchi(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_oquvchi.delete('/{id}',  status_code = 200)
def oquvchi_delete(id: int = 0,db: Session = Depends(get_db), current_user: TeacherCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id:
        return delete_oquvchi(id, db)