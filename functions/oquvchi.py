from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.oquvchi import Oquvchi
import datetime
from functions.fanlar import one_fan
from utils.pagination import pagination


def all_oquvchi(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Oquvchi.ism.like(search_formatted) | \
                        Oquvchi.familiya.like(search_formatted) | \
                        Oquvchi.tel.like(search_formatted) | \
                        Oquvchi.yosh.like(search_formatted) | \
                        Oquvchi.address.like(search_formatted) | \
                        Oquvchi.fan.like(search_formatted) | \
                        Oquvchi.vaqt.like(search_formatted) | \
                        Oquvchi.soat.like(search_formatted)
    else:
        search_filter = Oquvchi.id > 0

    if status in [True, False]:
        status_filter = Oquvchi.status == status
    else:
        status_filter = Oquvchi.status.in_([True, False])

    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyy-mmm-dd formatida yozing")
    dones = db.query(Oquvchi).options(joinedload(Oquvchi.tolov_id1)).options(joinedload(Oquvchi.subject)).options(joinedload(Oquvchi.kurs_sanalari4)).filter(Oquvchi.date > start_date).filter(
        Oquvchi.date <= end_date).filter(search_filter, status_filter).order_by(Oquvchi.id.desc())
    if page and limit:
        return pagination(dones, page, limit)
    else:
        return dones.all()


def one_oquvchi(ism, db):
    oquvchi = db.query(Oquvchi).filter(Oquvchi.id == ism).first()
    return oquvchi


def add_oquvchi(form, user, db):
    if one_fan(form.fan_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday fan mavjud emas")
    new_oquvchi = Oquvchi(
        ism=form.ism,
        tel=form.tel,
        familiya=form.familiya,
        yosh=form.yosh,
        address=form.address,
        fan_id=form.fan_id,
        soat=form.soat,
        user_id=user.id
    )
    db.add(new_oquvchi)
    db.commit()
    db.refresh(new_oquvchi)
    return {"date": "oquvchi saqlandi"}


def read_oquvchi(db):
    oquvchi = db.query(Oquvchi).all()
    return oquvchi


def update_oquvchi(form, oquvchi, db):
    if one_oquvchi(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli oquvchi mavjud emas")

    if one_oquvchi(form.ism, db) is None:
        raise HTTPException(status_code=400, detail="Bunday ismli oquvchi mavjud emas")
    oquvchi = db.query(Oquvchi).filter(Oquvchi.id == form.id).update(
        {
            Oquvchi.id: form.id,
            Oquvchi.ism: form.ism,
            Oquvchi.familiya: form.familiya,
            Oquvchi.tel: form.tel,
            Oquvchi.yosh: form.yosh,
            Oquvchi.address: form.address,
            Oquvchi.fan: form.fan,
            Oquvchi.vaqt: form.vaqt,
            Oquvchi.soat: form.soat,

        }
    )
    db.commit()
    return {"date": "Ma'lumot o'zgartirildi"}


def delete_oquvchi(id, db):
    oquvchi = db.query(Oquvchi).filter(Oquvchi.id == id).update(
        {
            Oquvchi.status: False
        }
    )
    db.commit()
    return {'date': "Ma'lumot o'chirildi"}

