# import form as form
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.fanlar import one_fan
from models.tolov import Tolov
import datetime
from functions.oquvchi import one_oquvchi
from utils.pagination import pagination


def all_tolov(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Tolov.fan_id.like(search_formatted) | \
                        Tolov.oquvchi_id.like(search_formatted) | \
                        Tolov.price.like(search_formatted) | \
                        Tolov.type.like(search_formatted) | \
                        Tolov.oy.like(search_formatted)

    else:
        search_filter = Tolov.id > 0

    if status in [True, False]:
        status_filter = Tolov.status == status
    else:
        status_filter = Tolov.status.in_([True, False])

    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyy-mmm-dd formatida yozing")
    dones = db.query(Tolov).options(joinedload(Tolov.tekshirish)).options(
        joinedload(Tolov.oquvchi_id1)).filter(Tolov.date > start_date).filter(
        Tolov.date <= end_date).filter(search_filter, status_filter).order_by(Tolov.id.desc())
    if page and limit:
        return pagination(dones, page, limit)
    else:
        return dones.all()


def one_tolov(type, db):
    product = db.query(Tolov).filter(Tolov.type == type).first()
    return product


def add_tolov(form, user, db):
    if one_oquvchi(form.oquvchi_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli oquvchi mavjud emas")
    if one_fan(form.fan_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli fan mavjud emas")
    new_tolov = Tolov(
        fan_id=form.fan_id,
        oquvchi_id=form.oquvchi_id,
        oy=form.oy,
        type=form.type,
        price=form.price,
        user_id=user.id
    )
    db.add(new_tolov)
    db.commit()
    db.refresh(new_tolov)
    return {"date": "tolov saqlandi"}


def read_tolov(db):
    tolov = db.query(Tolov).all()
    return tolov


def update_tolov(form, user, db):
    if one_tolov(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli tolov mavjud emas")

    if one_tolov(user.ism, db) is None:
        raise HTTPException(status_code=400, detail="Bunday ismli tolov mavjud emas")

    product = db.query(Tolov).filter(Tolov.id == form.id).update(
        {
            Tolov.id: form.id,
            Tolov.fan_id: form.fan_id,
            Tolov.oquvchi_id: form.oquvchi_id,
            Tolov.oy: form.oy,
            Tolov.price: form.price,
            Tolov.type: form.type,
        }
    )
    db.commit()
    return {"date": "Ma'lumot o'zgartirildi"}


def delete_tolov(id,db):
    db.query(Tolov).filter(Tolov.id == id).update({
        Tolov.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}

# def user_current(user, db):
#     return db.query(Products) .filter(Products.id == user.id).first()
