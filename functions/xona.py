from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.xona import Xona
import datetime

from utils.pagination import pagination
# from functions.kurs_sanalari import one_kurs_sanalari

def all_xona(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Xona.xona_nomi.like(search_formatted) | \
                        Xona.raqami.like(search_formatted)

    else:
        search_filter = Xona.id > 0

    if status in [True, False]:
        status_filter = Xona.status == status
    else:
        status_filter = Xona.status.in_([True, False])

    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyy-mmm-dd formatida yozing")
    dones = db.query(Xona).options(joinedload(Xona.kurs_sanalari3)).filter(Xona.date > start_date).filter(
        Xona.date <= end_date).filter(search_filter, status_filter).order_by(Xona.id.desc())
    if page and limit:
        return pagination(dones, page, limit)
    else:
        return dones.all()


def one_xona(xona, db):
    xona = db.query(Xona).filter(Xona.id == xona).first()
    return xona


def add_xona(form, user, db):
    # if one_xona(form.nomi, db) is None:
    #     raise HTTPException(status_code=400, detail="Bunday xona mavjud emas")
    new_xona = Xona(
        xona_nomi=form.xona_nomi,
        raqami=form.raqami,
        user_id=user.id
    )
    db.add(new_xona)
    db.commit()
    db.refresh(new_xona)
    return {"date": "Mahsulot saqlandi"}


def read_xona(db):
    xona = db.query(Xona).all()
    return xona


def update_xona(form, teacher, db):
    # if one_xona(form.id, db) is None:
    #     raise HTTPException(status_code=400, detail="Bunday id raqamli product mavjud emas")
    #
    # if one_xona(teacher.nomi, db) is None:
    #     raise HTTPException(status_code=400, detail="Bunday id raqamli product mavjud emas")
    xona = db.query(Xona).filter(Xona.id == form.id).update(
        {
            Xona.id: form.id,
            Xona.xona_nomi: form.xona_nomi,
            Xona.raqami: form.raqami,
        }
    )
    db.commit()
    return {"date": "Ma'lumot o'zgartirildi"}


def delete_xona(id, db):
    xona = db.query(Xona).filter(Xona.id == id).update(
        {
            Xona.status: False
        }
    )
    db.commit()
    return {'date': "Ma'lumot o'chirildi"}






