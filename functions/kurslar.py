from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.tolov import one_tolov
from models.kurslar import Kurslar
import datetime
from functions.teacher import one_teacher
from utils.pagination import pagination
from functions.fanlar import one_fan

def all_kurslar(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Kurslar.kurs_mudddati.like(search_formatted) | \
                        Kurslar.teacher_id.like(search_formatted) | \
                        Kurslar.fan_id.like(search_formatted) | \
                        Kurslar.vaqt.like(search_formatted) | \
                        Kurslar.soat.like(search_formatted)
    else:
        search_filter = Kurslar.id > 0

    if status in [True, False]:
        status_filter = Kurslar.status == status
    else:
        status_filter = Kurslar.status.in_([True, False])

    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyy-mmm-dd formatida yozing")
    dones = db.query(Kurslar).options(joinedload(Kurslar.fan_id2)).options(joinedload(Kurslar.teacher_id2)).filter(Kurslar.date > start_date).filter(
        Kurslar.date <= end_date).filter(search_filter, status_filter).order_by(Kurslar.id.desc())
    if page and limit:
        return pagination(dones, page, limit)
    else:
        return dones.all()


def one_kurslar(kurs, db):
    kurslar = db.query(Kurslar).filter(Kurslar.kurs_muddati == kurs).first()
    return kurslar


def add_kurslar(form, user, db):
    if one_teacher(form.teacher_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday oqituvchi mavjud emas")
    if one_fan(form.fan_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday fan mavjud emas")

    new_kurslar = Kurslar(
        fan_id=form.fan_id,
        teacher_id=form.teacher_id,
        soat=form.soat,
        kurs_muddati=form.kurs_muddati,
        user_id=user.id
    )
    db.add(new_kurslar)
    db.commit()
    db.refresh(new_kurslar)
    return {"date": "kurs saqlandi"}


def read_kurslar(db):
    kurslar = db.query(Kurslar).all()
    return kurslar


def update_kurslar(form, kurslar, db):
    if one_kurslar(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli kurs mavjud emas")

    if one_kurslar(form.kurs_muddati , db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli kurs_muddati mavjud emas")
    kurslar = db.query(Kurslar).filter(Kurslar.id == form.id).update(
        {
            Kurslar.id: form.id,
            Kurslar.fan_id: form.fan_id,
            Kurslar.teacher_id: form.teacher_id,
            Kurslar.kurs_muddati: form.kurs_muddati,
            Kurslar.vaqt: form.vaqt,
            Kurslar.soat: form.soat,

        }
    )
    db.commit()
    return {"date": "Ma'lumot o'zgartirildi"}


def delete_kurslar(id, db):
    kurs = db.query(Kurslar).filter(Kurslar.id == id).update(
        {
            Kurslar.status: False
        }
    )
    db.commit()
    return {'date': "Ma'lumot o'chirildi"}

