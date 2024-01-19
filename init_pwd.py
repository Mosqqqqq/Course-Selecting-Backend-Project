from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session
from database.models5 import *
from apps.tools import *

engine = create_engine(url='mysql://root:' + SQL_PWD + '@localhost/my_school')

encryption_key = open('./apps/login/pwd.key', 'rb').read()
with Session(bind=engine) as conn:
    query = conn.query(Student.student_id)
    for tup in query.all():
        encrypted_str = encrypt_string(tup[0], encryption_key)
        query = update(Student).where(get_where_conditions(Student.__table__.columns.values(), tup[0])).values(
            **get_update_dict(['pwd'], [encrypted_str]))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            print(e)

with Session(bind=engine) as conn:
    query = conn.query(Staff.staff_id)
    for tup in query.all():
        encrypted_str = encrypt_string(tup[0], encryption_key)
        query = update(Staff).where(get_where_conditions(Staff.__table__.columns.values(), tup[0])).values(
            **get_update_dict(['pwd'], [encrypted_str]))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            print(e)
