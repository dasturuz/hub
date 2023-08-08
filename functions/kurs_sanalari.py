from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.xona import one_xona
from models.kurs_sanalari import Kurs_sanalari
import datetime
from functions.fanlar import one_fan
from utils.pagination import pagination
from functions.teacher import one_teacher
from functions.xona import one_xona
from functions.oquvchi import one_oquvchi

def all_kurs_sanalari(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Kurs_sanalari.xona_id.like(search_formatted) | \
                        Kurs_sanalari.teacher_id.like(search_formatted) | \
                        Kurs_sanalari.fan_id.like(search_formatted) | \
                        Kurs_sanalari.vaqt.like(search_formatted) | \
                        Kurs_sanalari.oquvchi_id.like(search_formatted) | \
                        Kurs_sanalari.bor_yoq.like(search_formatted) | \
                        Kurs_sanalari.boshi.like(search_formatted) | \
                        Kurs_sanalari.oxiri.like(search_formatted) | \
                        Kurs_sanalari.soat.like(search_formatted)
    else:
        search_filter = Kurs_sanalari.id > 0

    if status in [True, False]:
        status_filter = Kurs_sanalari.status == status
    else:
        status_filter = Kurs_sanalari.status.in_([True, False])

    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyy-mmm-dd formatida yozing")
    dones = db.query(Kurs_sanalari).options(joinedload(Kurs_sanalari.fan_id3))\
        .options(joinedload(Kurs_sanalari.teacher_id3)).options(joinedload(Kurs_sanalari.xona_id1)).options(joinedload(Kurs_sanalari.oquvchi_id2)).filter(Kurs_sanalari.date > start_date).filter(
        Kurs_sanalari.date <= end_date).filter(search_filter, status_filter).order_by(Kurs_sanalari.id.desc())
    if page and limit:
        return pagination(dones, page, limit)
    else:
        return dones.all()


def one_kurs_sanalari(vaqt, db):
    kurs_sanalari = db.query(Kurs_sanalari).filter(Kurs_sanalari.vaqt == vaqt).first()
    return kurs_sanalari


def add_kurs_sanalari(form, user, db):
    if one_fan(form.fan_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday fan mavjud emas")
    if one_teacher(form.teacher_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday oqituvchi mavjud emas")
    if one_xona(form.xona_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday xona mavjud emas")
    if one_oquvchi(form.oquvchi_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday oquvchi mavjud emas")
    new_kurs_sanalari = Kurs_sanalari(
        fan_id=form.fan_id,
        teacher_id=form.teacher_id,
        bor_yoq=form.bor_yoq,
        boshi=form.boshi,
        oxiri=form.oxiri,
        soat=form.soat,
        xona_id=form.xona_id,
        oquvchi_id=form.oquvchi_id,
        user_id=user.id
    )
    db.add(new_kurs_sanalari)
    db.commit()
    db.refresh(new_kurs_sanalari)
    return {"date": "kurs sanasi saqlandi"}


def read_kurs_sanalari(db):
    kurs_sanalari = db.query(Kurs_sanalari).all()
    return kurs_sanalari


def update_kurs_sanalari(form, kurs_sanlari, db):
    if one_kurs_sanalari(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli kurs sanasi mavjud emas")
    user_verification = db.query(Kurs_sanalari).filter(Kurs_sanalari.id == form.id).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday kurs sanasi mavjud")



    kurs_sanlari = db.query(Kurs_sanalari).filter(Kurs_sanalari.id == form.id).update(
        {
            Kurs_sanalari.id: form.id,
            Kurs_sanalari.fan_id: form.fan_id,
            Kurs_sanalari.teacher_id: form.teacher_id,
            Kurs_sanalari.oquvchi_id: form.oquvchi_id,
            Kurs_sanalari.bor_yoq: form.bor_yoq,
            Kurs_sanalari.boshi: form.boshi,
            Kurs_sanalari.oxiri: form.oxiri,
            Kurs_sanalari.xona_id: form.xona_id,
            Kurs_sanalari.vaqt: form.vaqt,
            Kurs_sanalari.soat: form.soat,

        }
    )
    db.commit()
    return {"date": "Ma'lumot o'zgartirildi"}


def delete_kurs_sanalari(id, db):
    kurs_sanalari = db.query(Kurs_sanalari).filter(Kurs_sanalari.id == id).update(
        {
            Kurs_sanalari.status: False
        }
    )
    db.commit()
    return {'date': "Ma'lumot o'chirildi"}

