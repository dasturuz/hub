from passlib.context import CryptContext
from sqlalchemy.orm import joinedload

pwd_context = CryptContext(schemes=['bcrypt'])

from fastapi import HTTPException
from models.teacher import Teacher

from routes.auth import get_password_hash
from utils.pagination import pagination


def all_teacher(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Teacher.ism.like(search_formatted) | Teacher.tel.like(search_formatted) |  Teacher.familiya.like(search_formatted)
    else:
        search_filter = Teacher.id > 0
    if status in [True, False]:
        status_filter = Teacher.status == status
    else:
        status_filter = Teacher.id > 0

    if roll:
        roll_filter = Teacher.roll == roll
    else:
        roll_filter = Teacher.id > 0

    teacher = db.query(Teacher).options(joinedload(Teacher.fan_id1)).options(joinedload(Teacher.kurs_id2)).options(joinedload(Teacher.kurs_sanalari2)).options(joinedload(Teacher.chiqimlar_id1)).filter(
        search_filter, status_filter, roll_filter).order_by(Teacher.ism.asc())
    if page and limit:
        return pagination(teacher, page, limit)
    else:
        return teacher.all()


def one_teacher(id, db):
    return db.query(Teacher).filter(Teacher.id == id).first()


def teacher_current(teacher, db):
    return db.query(Teacher).filter(Teacher.id == teacher.id).first()


def create_teacher(form, teacher, db):
    teacher_verification = db.query(Teacher).filter(Teacher.tel == form.tel).first()
    if teacher_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
    # number_verification = db.query(Teacher).filter(Teacher.fan_id == form.fan_id).first()
    # if number_verification:
    #     raise HTTPException(status_code=400, detail="Bunday telefon raqami  mavjud emas")

    new_teacher_db = Teacher(
        ism=form.ism,
        familiya=form.familiya,
        tel=form.tel,
        user_id = teacher.id,
        password=get_password_hash(form.password),
        fan_id=form.fan_id,
    )
    db.add(new_teacher_db)
    db.commit()
    db.refresh(new_teacher_db)

    return new_teacher_db


def update_teacher(form, teacher, db):
    if one_teacher(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    teacher_verification = db.query(Teacher).filter(Teacher.tel == form.tel).first()
    if teacher_verification and teacher_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

    db.query(Teacher).filter(Teacher.id == form.id).update({
        Teacher.ism: form.ism,
        Teacher.familiya: form.familiya,
        Teacher.password: get_password_hash(form.password),
        Teacher.fan_id: form.fan_id,
        Teacher.user_id: form.user_id,
        Teacher.tel: form.tel,

    })
    db.commit()

    return one_teacher(form.id, db)




def teacher_delete(id, db):
    if one_teacher(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Teacher).filter(Teacher.id == id).update({
        Teacher.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
