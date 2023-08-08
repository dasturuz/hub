
import datetime
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
from pydantic.datetime_parse import date
from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.teacher import teacher_current
from functions.fanlar import one_fan, all_fan, update_fan, add_fan, delete_fan
from schemas.fanlar import FanBase,FanCreate,FanUpdate
from schemas.teacher import TeacherCurrent
router_fan = APIRouter()



@router_fan.post("/add")
def fan_qoshish(form:FanCreate,db:Session=Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user)):
    return add_fan(form=form,user=current_user,db=db)


@router_fan.get('/',  status_code = 200)
def get_fan(search:str=None,status:bool=True,id:int=0,start_date:date=datetime.datetime.now().date().min,end_date:date=datetime.datetime.now().date(),page:int=1,limit:int=2, db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_fan(id, db)
    else :
        return all_fan(search=search,status=status,start_date=start_date,end_date=end_date,page=page,limit=limit,db=db)




@router_fan.put("/update")
def fan_update(form: FanUpdate, db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user)) :
    if update_fan(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_fan.delete('/{id}',  status_code = 200)
def fan_delete(id: int = 0,db: Session = Depends(get_db), current_user: TeacherCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id:
        return delete_fan(id, db)