from db import SessionLocal
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session

from models import Teacher
from routes import teacher,auth
from db import Base, engine
import datetime
from routes import tolov,xona,oquvchi,kurslar,kurs_sanalari,fanlar,chiqimlar
from routes.auth import get_password_hash

Base.metadata.create_all(bind=engine)

app=FastAPI(
	title="Modmi",
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.get('/')
def home():
	return {"message": "welcome to fastapi "}


app.include_router(
	auth.login_router,
	prefix='/auth',
	tags=['teacher auth section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)

app.include_router(
	teacher.router_teacher,
	prefix='/teacher',
	tags=['teacher section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)
app.include_router(
	tolov.router_tolov,
	prefix='/tolov',
	tags=['tolov section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)

app.include_router(
	xona.router_xona,
	prefix='/xona',
	tags=['xona section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)

app.include_router(
	oquvchi.router_oquvchi,
	prefix='/oquvchi',
	tags=['oquvchi section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)

app.include_router(
	kurslar.router_kurslar,
	prefix='/kurslar',
	tags=['kurslar section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)

app.include_router(
	kurs_sanalari.router_kurs_sanalari,
	prefix='/kurs_sanalari',
	tags=['kurs_sanalari section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)

app.include_router(
	fanlar.router_fan,
	prefix='/fanlar',
	tags=['fanlar section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)

app.include_router(
	chiqimlar.router_chiqimlar,
	prefix='/chiqimlar',
	tags=['chiqimlar section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)

try:
	db=SessionLocal()
	new_user_db = Teacher(
      ism = 'www',
      tel = 'www',
	  fan_id = '111',
      password = get_password_hash('000'),
      familiya = 'www',
      status = True,
	  user_id = '1',

	 )

	db.add(new_user_db)
	db.commit()
	db.refresh(new_user_db)
except Exception as x:
	print(x,'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
