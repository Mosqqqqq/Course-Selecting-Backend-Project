from fastapi import APIRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database.models7 import *
from apps.tools import *
from typing import Union

login_urls = APIRouter()
engine = create_engine(url='mysql://root:' + SQL_PWD + '@localhost/my_school')
encryption_key = open('./apps/login/pwd.key', 'rb').read()


@login_urls.get('/student', summary='student login')
def student_login(student_id: Union[str, None] = None, pwd: Union[str, None] = None):
    if student_id is None or pwd is None:
        return {'msg': 'not enough information.', 'pass': 0}
    with Session(bind=engine) as conn:
        query = conn.query(Student.pwd).where(get_where_conditions(Student.__table__.columns.values(), student_id))
        if len(query.all()) == 0:
            return {'msg': 'student not exist.'}
        check_str = decrypt_string(query.all()[0][0], encryption_key)
        if str(check_str) == pwd:
            return {'msg': 'correct pwd.', 'pass': 1}
        else:
            return {'msg': 'wrong pwd.', 'pass': 0}


@login_urls.get('/staff', summary='staff login')
def staff_login(staff_id: Union[str, None] = None, pwd: Union[str, None] = None):
    if staff_id is None or pwd is None:
        return {'msg': 'not enough information.', 'pass': 0}
    with Session(bind=engine) as conn:
        query = conn.query(Staff.pwd).where(get_where_conditions(Staff.__table__.columns.values(), staff_id))
        if len(query.all()) == 0:
            return {'msg': 'staff not exist.'}
        check_str = decrypt_string(query.all()[0][0], encryption_key)
        if str(check_str) == pwd:
            return {'msg': 'correct pwd.', 'pass': 1}
        else:
            return {'msg': 'wrong pwd.', 'pass': 0}


@login_urls.get('/root', summary='root login')
def root_login(root_id: Union[str, None] = None, pwd: Union[str, None] = None):
    if root_id is None or pwd is None:
        return {'msg': 'not enough information.', 'pass': 0}
    with Session(bind=engine) as conn:
        query = conn.query(Root.pwd).where(get_where_conditions(Root.__table__.columns.values(), root_id))
        if len(query.all()) == 0:
            return {'msg': 'root account not exist.'}
        check_str = decrypt_string(query.all()[0][0], encryption_key)
        if str(check_str) == pwd:
            return {'msg': 'correct pwd.', 'pass': 1}
        else:
            return {'msg': 'wrong pwd.', 'pass': 0}
