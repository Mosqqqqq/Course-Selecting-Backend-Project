from fastapi import APIRouter
from sqlalchemy import create_engine, update, delete, insert
from sqlalchemy.orm import Session
from database.models5 import *
from apps.tools import *
from apps.root.updateinfo_root import *

root_urls_delete = APIRouter()
engine = create_engine(url='mysql://root:zsqlmm@localhost/my_school')


@root_urls_delete.delete('/delete_dept', summary='delete dept')
def delete_dept(dept_id: Union[str, None] = None):
    if dept_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Dept.dept_id).where(get_where_conditions(list(Dept.__table__.columns.values()), dept_id))
        if len(query.all()) == 0:
            return {'msg': 'nothing to delete.'}
        query = delete(Dept).where(get_where_conditions(list(Dept.__table__.columns.values()), dept_id))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_delete.delete('/delete_major', summary='delete major')
def delete_major(major_id: Union[str, None] = None):
    if major_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Major.major_id).where(get_where_conditions(list(Major.__table__.columns.values()), major_id))
        if len(query.all()) == 0:
            return {'msg': 'nothing to delete.'}
        query = delete(Major).where(get_where_conditions(list(Major.__table__.columns.values()), major_id))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_delete.delete('/delete_class', summary='delete class')
def delete_class(class_id: Union[str, None] = None):
    if class_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Clas.class_id).where(get_where_conditions(list(Clas.__table__.columns.values()), class_id))
        if len(query.all()) == 0:
            return {'msg': 'nothing to delete.'}
        query = delete(Clas).where(get_where_conditions(list(Clas.__table__.columns.values()), class_id))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_delete.delete('/delete_student', summary='delete student')
def delete_student(student_id: Union[str, None] = None):
    if student_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Student.student_id).where(
            get_where_conditions(list(Student.__table__.columns.values()), student_id))
        if len(query.all()) == 0:
            return {'msg': 'nothing to delete.'}
        query = delete(Student).where(get_where_conditions(list(Student.__table__.columns.values()), student_id))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_delete.delete('/delete_staff', summary='delete staff')
def delete_staff(staff_id: Union[str, None] = None):
    if staff_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Staff.staff_id).where(
            get_where_conditions(list(Staff.__table__.columns.values()), staff_id))
        if len(query.all()) == 0:
            return {'msg': 'nothing to delete.'}
        query = delete(Staff).where(get_where_conditions(list(Staff.__table__.columns.values()), staff_id))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_delete.delete('/delete_all_course', summary='delete all_course')
def delete_all_course(course_id: Union[str, None] = None):
    if course_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(AllCourse.course_id).where(
            get_where_conditions(list(AllCourse.__table__.columns.values()), course_id))
        if len(query.all()) == 0:
            return {'msg': 'nothing to delete.'}
        query = delete(AllCourse).where(get_where_conditions(list(AllCourse.__table__.columns.values()), course_id))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_delete.delete('/delete_available_course', summary='delete available_course')
def delete_available_course(course_id: Union[str, None] = None, semester: Union[str, None] = None,
                            staff_id: Union[str, None] = None, class_time: Union[str, None] = None):
    if course_id is None or semester is None or staff_id is None or class_time is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(AvailableCourse.course_id).where(
            get_where_conditions(list(AvailableCourse.__table__.columns.values()), course_id, semester, staff_id,
                                 class_time))
        if len(query.all()) == 0:
            return {'msg': 'nothing to delete.'}
        query = delete(AvailableCourse).where(
            get_where_conditions(list(AvailableCourse.__table__.columns.values()), course_id, semester, staff_id,
                                 class_time))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_delete.delete('/delete_selected_course_now', summary='delete selected_course_now')
def delete_selected_course_now(student_id: Union[str, None] = None, semester: Union[str, None] = None,
                               course_id: Union[str, None] = None):
    if student_id is None or semester is None or course_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(SelectedCourseNow.course_id).where(
            get_where_conditions(list(SelectedCourseNow.__table__.columns.values()), student_id, semester, course_id))
        if len(query.all()) == 0:
            return {'msg': 'nothing to delete.'}
        query = delete(SelectedCourseNow).where(
            get_where_conditions(list(SelectedCourseNow.__table__.columns.values()), student_id, semester, course_id))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_delete.delete('/delete_ended_course', summary='delete ended course')
def delete_ended_course(student_id: Union[str, None] = None, semester: Union[str, None] = None,
                        course_id: Union[str, None] = None):
    if student_id is None or semester is None or course_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(EndedCourse.course_id).where(
            get_where_conditions(list(EndedCourse.__table__.columns.values()), student_id, semester, course_id))
        if len(query.all()) == 0:
            return {'msg': 'nothing to delete.'}
        query = delete(EndedCourse).where(
            get_where_conditions(list(EndedCourse.__table__.columns.values()), student_id, semester, course_id))
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}
