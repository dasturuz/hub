from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.chiqimlar import Chiqimlar
import datetime
from functions.teacher import one_teacher
from utils.pagination import pagination


def all_chiqimlar(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Chiqimlar.money.like(search_formatted) | \
                        Chiqimlar.teacher_id.like(search_formatted) | \
                        Chiqimlar.comment.like(search_formatted) | \
                        Chiqimlar.type.like(search_formatted)
    else:
        search_filter = Chiqimlar.id > 0

    if status in [True, False]:
        status_filter = Chiqimlar.status == status
    else:
        status_filter = Chiqimlar.status.in_([True, False])

    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyy-mmm-dd formatida yozing")
    dones = db.query(Chiqimlar).options(joinedload(Chiqimlar.teacher_id4)).filter(Chiqimlar.date > start_date).filter(
        Chiqimlar.date <= end_date).filter(search_filter, status_filter).order_by(Chiqimlar.id.desc())
    if page and limit:
        return pagination(dones, page, limit)
    else:
        return dones.all()


def one_chiqimlar(chiqim, db):
    chiqim = db.query(Chiqimlar).filter(Chiqimlar.money == chiqim).first()
    return chiqim


def add_chiqimlar(form, user, db):
    if one_teacher(form.teacher_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday ustoz mavjud emas")

    new_chiqimlar = Chiqimlar(
        money=form.money,
        teacher_id=form.teacher_id,
        comment=form.comment,
        type=form.type,
        user_id=user.id,
        currency=form.currency
    )
    db.add(new_chiqimlar)
    db.commit()
    db.refresh(new_chiqimlar)
    return {"date": "chiqim saqlandi"}


def read_chiqimlar(db):
    chiqimlar = db.query(Chiqimlar).all()
    return chiqimlar


def update_chiqimlar(form, chiqimlar, db):
    if one_chiqimlar(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli chiqim mavjud emas")
    user_verification = db.query(Chiqimlar).filter(Chiqimlar.id == form.id).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday chiqim mavjud")

    chiqimlar = db.query(Chiqimlar).filter(Chiqimlar.id == form.id).update(
        {
            Chiqimlar.id: form.id,
            Chiqimlar.money: form.money,
            Chiqimlar.teacher_id: form.teacher_id,
            Chiqimlar.comment: form.comment,
            Chiqimlar.type: form.type,
        }
    )
    db.commit()
    return {"date": "Ma'lumot o'zgartirildi"}


def delete_chiqimlar(id, db):

    chiqim = db.query(Chiqimlar).filter(Chiqimlar.id == id).update(
        {
            Chiqimlar.status: False
        }
    )
    db.commit()
    return {'date': "Ma'lumot o'chirildi"}

