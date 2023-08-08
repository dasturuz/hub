
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user


Base.metadata.create_all(bind=engine)


from functions.teacher import one_teacher, all_teacher, update_teacher, create_teacher, teacher_delete,teacher_current
from schemas.teacher import TeacherBase,TeacherCreate,TeacherUpdate,TeacherCurrent

router_teacher = APIRouter()



@router_teacher.post('/add', )
def add_teacher(form: TeacherCreate, db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user) ) : #
    if create_teacher(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_teacher.get('/',  status_code = 200)
def get_teachers(search: str = None, status: bool = True, id: int = 0,roll : str = None, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_teacher(id, db)
    else :
        return all_teacher(search, status,roll, page, limit, db)

@router_teacher.get('/user',  status_code = 200)
def get_teacher_current(db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if current_user:
        return teacher_current(current_user, db)


@router_teacher.put("/update")
def user_update(form: TeacherUpdate, db: Session = Depends(get_db),current_user: TeacherCurrent = Depends(get_current_active_user)) :
    if update_teacher(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_teacher.delete('/{id}',  status_code = 200)
def delete_teacher(id: int = 0,db: Session = Depends(get_db), current_user: TeacherCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id:
        return teacher_delete(id, db)