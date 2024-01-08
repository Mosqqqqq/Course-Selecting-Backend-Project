from fastapi import APIRouter
from sqlalchemy import create_engine, update, delete, insert
from sqlalchemy.orm import Session
from database.models6 import *
from apps.tools import *
from apps.root.updateinfo_root import *

root_urls_update = APIRouter()
engine = create_engine(url='mysql://root:zsqlmm@localhost/my_school')


@root_urls_update.put('/update_dept', summary='update dept')
def update_dept(update_info: UpdateInfoDept, dept_id: Union[str, None] = None):
    if dept_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Dept.dept_id).where(Dept.dept_id == update_info.dept_id)
        if len(query.all()) == 0:
            return {'msg': 'dept_id does not exists.'}
        query = update(Dept).where(get_where_conditions(Dept.__table__.columns.values(), dept_id)) \
            .values(
            **get_update_dict(list(Dept.__table__.columns.keys()), [update_info.dept_id, update_info.dept_name]))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_update.put('/update_major', summary='update major')
def update_major(update_info: UpdateInfoMajor, major_id: Union[str, None] = None):
    if major_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Major.major_id).where(Major.major_id == update_info.major_id)
        if len(query.all()) == 0:
            return {'msg': 'major_id does not exists.'}
        query = update(Major).where(
            get_where_conditions(Major.__table__.columns.values(), major_id)) \
            .values(**get_update_dict(list(Major.__table__.columns.keys()),
                                      [update_info.major_id, update_info.dept_id, update_info.major_name]))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_update.put('/update_class', summary='update class')
def update_class(update_info: UpdateInfoClass, class_id: Union[str, None] = None):
    if class_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Clas.class_id).where(Clas.class_id == update_info.class_id)
        if len(query.all()) == 0:
            return {'msg': 'class_id does not exists.'}
        query = update(Clas).where(
            get_where_conditions(Clas.__table__.columns.values(), class_id)) \
            .values(**get_update_dict(list(Clas.__table__.columns.keys()),
                                      [update_info.class_id, update_info.dept_id, update_info.major_id,
                                       update_info.class_name]))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_update.put('/update_student', summary='update student')
def update_student(update_info: UpdateInfoStudent, student_id: Union[str, None] = None):
    if student_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Student.student_id).where(Student.student_id == update_info.student_id)
        if len(query.all()) == 0:
            return {'msg': 'student_id does not exists.'}
        encryption_key = open('./apps/login/pwd.key', 'rb').read()
        encrypted_str = encrypt_string(update_info.student_id, encryption_key)
        query = update(Student).where(
            get_where_conditions(Student.__table__.columns.values(), student_id)) \
            .values(**get_update_dict(list(Student.__table__.columns.keys()),
                                      [update_info.student_id, update_info.major_id, update_info.dept_id,
                                       update_info.class_id, update_info.student_name, update_info.sex,
                                       update_info.grade, None, None, encrypted_str]))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_update.put('/update_student_gpa', summary='update student gpa')
def update_student_gpa():
    with engine.connect() as connection:
        try:
            connection.execute("CALL cal_gpa()")
            return {'msg': 'success'}
        except Exception as e:
            return {'msg': str(e)}


@root_urls_update.put('/update_staff', summary='update staff')
def update_staff(update_info: UpdateInfoStaff, staff_id: Union[str, None] = None):
    if staff_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Staff.staff_id).where(Staff.staff_id == update_info.staff_id)
        if len(query.all()) == 0:
            return {'msg': 'staff_id does not exists.'}
        query = update(Staff).where(
            get_where_conditions(Staff.__table__.columns.values(), staff_id)) \
            .values(**get_update_dict(list(Staff.__table__.columns.keys()),
                                      [update_info.staff_id, update_info.dept_id, update_info.staff_name,
                                       update_info.sex, update_info.date_of_birth, update_info.ranks,
                                       update_info.salary]))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_update.put('/update_all_course', summary='update all_course')
def update_all_course(update_info: UpdateInfoAllCourse, course_id: Union[str, None] = None):
    if course_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(AllCourse.course_id).where(AllCourse.course_id == update_info.course_id)
        if len(query.all()) == 0:
            return {'msg': 'course_id does not exists.'}
        query = update(AllCourse).where(
            get_where_conditions(AllCourse.__table__.columns.values(), course_id)) \
            .values(**get_update_dict(list(AllCourse.__table__.columns.keys()),
                                      [update_info.course_id, update_info.course_name, update_info.credit,
                                       update_info.course_hours, update_info.dept_id]))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_update.put('/update_available_course', summary='update available_course')
def update_available_course(update_info: UpdateInfoAvailableCourse, course_id: Union[str, None] = None,
                            semester: Union[str, None] = None, staff_id: Union[str, None] = None,
                            class_time: Union[str, None] = None):
    if course_id is None or semester is None or staff_id is None or class_time is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(AvailableCourse.course_id).where(
            get_where_conditions(AvailableCourse.__table__.columns.values(), course_id, semester, staff_id, class_time))
        if len(query.all()) == 0:
            return {'msg': 'course is not available.'}
        query = update(AvailableCourse).where(
            get_where_conditions(AvailableCourse.__table__.columns.values(), course_id, semester, staff_id, class_time)) \
            .values(**get_update_dict(list(AvailableCourse.__table__.columns.keys()),
                                      [update_info.course_id, update_info.semester, update_info.staff_id,
                                       update_info.class_time, update_info.class_time, update_info.class_place]))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}
