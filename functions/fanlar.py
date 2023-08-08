from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.fanlar import Fan
import datetime

from utils.pagination import pagination


def all_fan(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Fan.xona_nomi.like(search_formatted)

    else:
        search_filter = Fan.id > 0

    if status in [True, False]:
        status_filter = Fan.status == status
    else:
        status_filter = Fan.status.in_([True, False])

    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyy-mmm-dd formatida yozing")
    dones = db.query(Fan).options(joinedload(Fan.mablag)).options(joinedload(Fan.teacher_id1)).options(joinedload(Fan.kurs_id1)).options(joinedload(Fan.student)).options(joinedload(Fan.kurs_sanalari1)).filter(Fan.date > start_date).filter(
        Fan.date <= end_date).filter(search_filter, status_filter).order_by(Fan.id.desc())
    if page and limit:
        return pagination(dones, page, limit)
    else:
        return dones.all()


def one_fan(fan, db):
    fan = db.query(Fan).filter(Fan.id == fan).first()
    return fan


def add_fan(form, user, db):
    # if one_fan(form.nomi, db) is None:
    #     raise HTTPException(status_code=400, detail="Bunday fan mavjud emas")
    new_fan = Fan(
        nomi=form.nomi,
        user_id=user.id
    )
    db.add(new_fan)
    db.commit()
    db.refresh(new_fan)
    return {"date": "fan saqlandi"}


def read_fan(db):
    fan = db.query(Fan).all()
    return fan


def update_fan(form,  db):
    # if one_fan(form.id, db) is None:
    #     raise HTTPException(status_code=400, detail="Bunday id raqamli fan mavjud emas")
    #
    # if one_fan(form.nomi, db) is None:
    #     raise HTTPException(status_code=400, detail="Bunday id raqamli fan mavjud emas")
    fan = db.query(Fan).filter(Fan.id == form.id).update(
        {
            Fan.id: form.id,
            Fan.nomi: form.nomi,

        }
    )
    db.commit()
    return {"date": "Ma'lumot o'zgartirildi"}


def delete_fan(id, db):
    fan = db.query(Fan).filter(Fan.id == id).update(
        {
            Fan.status: False
        }
    )
    db.commit()
    return {'date': "Ma'lumot o'chirildi"}






