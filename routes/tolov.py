
import datetime
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
from pydantic.datetime_parse import date
from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.teacher import teacher_current
from functions.tolov import one_tolov, all_tolov, update_tolov, add_tolov, delete_tolov
from schemas.tolov import TolovBase,TolovCreate,TolovUpdate
from schemas.teacher import TeacherCurrent
router_tolov = APIRouter()



@router_tolov.post("/add")
def tolov_qoshish(form:TolovCreate,db:Session=Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user)):
    return add_tolov(form=form,user=current_user,db=db)


@router_tolov.get('/',  status_code = 200)
def get_tolov(search:str=None,status:bool=True,id:int=0,start_date:date=datetime.datetime.now().date().min,end_date:date=datetime.datetime.now().date(),page:int=1,limit:int=2, db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_tolov(id, db)
    else :
        return all_tolov(search=search,status=status,start_date=start_date,end_date=end_date,page=page,limit=limit,db=db)




@router_tolov.put("/update")
def tolov_update(form: TolovUpdate, db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user)) :
    if update_tolov(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_tolov.delete('/{id}',  status_code = 200)
def tolov_delete(id: int = 0,db: Session = Depends(get_db), current_user: TeacherCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id:
        return delete_tolov(id,db)