from fastapi import APIRouter
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session
from database.models7 import *
from apps.tools import *
from apps.root.updateinfo_root import *

root_urls_insert = APIRouter()
engine = create_engine(url='mysql://root:' + SQL_PWD + '@localhost/my_school')


@root_urls_insert.post('/insert_dept', summary='insert dept')
def insert_dept(dept_info: UpdateInfoDept):
    if dept_info.dept_id is None or dept_info.dept_name is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Dept.dept_id).where(
            get_where_conditions(Dept.__table__.columns.values(), dept_info.dept_id, None))
        if len(query.all()) >= 1:
            return {'msg': f'failed to insert, dept_id {query.all()[0][0]} already exists.'}
        insert_query = insert(Dept).values(
            [get_update_dict(Dept.__table__.columns.keys(), [dept_info.dept_id, dept_info.dept_name])])
        try:
            conn.execute(insert_query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_insert.post('/insert_major', summary='insert major')
def insert_major(major_info: UpdateInfoMajor):
    if major_info.major_id is None or major_info.dept_id is None or major_info.major_name is None:
        return {'msg': 'not enough information'}
    with Session(bind=engine) as conn:
        query = conn.query(Dept.dept_id).where(
            get_where_conditions(Dept.__table__.columns.values(), major_info.dept_id, None))
        if len(query.all()) == 0:
            return {'msg': f'failed to insert, dept_id {major_info.dept_id} does not exist.'}
        query = conn.query(Major.major_id).where(
            get_where_conditions(Major.__table__.columns.values(), major_info.major_id, None, None))
        if len(query.all()) >= 1:
            return {'msg': f'failed to insert, major_id {query.all()[0][0]} already exists.'}
        insert_query = insert(Major).values(
            [get_update_dict(Major.__table__.columns.keys(),
                             [major_info.major_id, major_info.dept_id, major_info.major_name])])
        try:
            conn.execute(insert_query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_insert.post('/insert_class', summary='insert class')
def insert_class(class_info: UpdateInfoClass):
    if class_info.class_id is None or class_info.dept_id is None or class_info.major_id is None or \
            class_info.class_name is None:
        return {'msg': 'not enough information'}
    with Session(bind=engine) as conn:
        query = conn.query(Dept.dept_id).where(
            get_where_conditions(Dept.__table__.columns.values(), class_info.dept_id, None))
        if len(query.all()) == 0:
            return {'msg': f'failed to insert, dept_id {class_info.dept_id} does not exist.'}
        query = conn.query(Major.major_id).where(
            get_where_conditions(Major.__table__.columns.values(), class_info.major_id, None, None))
        if len(query.all()) == 0:
            return {'msg': f'failed to insert, major_id {class_info.major_id} does not exist.'}
        query = conn.query(Clas.class_id).where(
            get_where_conditions(Clas.__table__.columns.values(), class_info.class_id, None, None, None))
        if len(query.all()) >= 1:
            return {'msg': f'failed to insert, class_id {query.all()[0][0]} already exists.'}
        insert_query = insert(Clas).values(
            [get_update_dict(Clas.__table__.columns.keys(),
                             [class_info.class_id, class_info.dept_id, class_info.major_id, class_info.class_name])])
        try:
            conn.execute(insert_query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_insert.post('/insert_student', summary='insert student')
def insert_student(student_info: UpdateInfoStudent):
    if student_info.student_id is None or student_info.major_id is None or student_info.dept_id is None or \
            student_info.class_id is None or student_info.student_name is None or student_info.sex is None or \
            student_info.grade is None:
        return {'msg': 'not enough information'}
    with Session(bind=engine) as conn:
        query = conn.query(Dept.dept_id).where(
            get_where_conditions(Dept.__table__.columns.values(), student_info.dept_id, None))
        if len(query.all()) == 0:
            return {'msg': f'failed to insert, dept_id {student_info.dept_id} does not exist.'}
        query = conn.query(Major.major_id).where(
            get_where_conditions(Major.__table__.columns.values(), student_info.major_id, None, None))
        if len(query.all()) == 0:
            return {'msg': f'failed to insert, major_id {student_info.major_id} does not exist'}
        query = conn.query(Clas.class_id).where(
            get_where_conditions(Clas.__table__.columns.values(), student_info.class_id, None, None, None))
        if len(query.all()) == 0:
            return {'msg': f'failed to insert, class_id {student_info.class_id} does not exist.'}
        query = conn.query(Student.student_id).where(
            get_where_conditions(Student.__table__.columns.values(), student_info.student_id, None, None, None, None,
                                 None, None))
        if len(query.all()) >= 1:
            return {'msg': f'failed to insert, student_id {query.all()[0][0]} already exists.'}
        encryption_key = open('./apps/login/pwd.key', 'rb').read()
        encrypted_str = encrypt_string(student_info.student_id, encryption_key)
        insert_query = insert(Student).values(
            [get_update_dict(Student.__table__.columns.keys(),
                             [student_info.student_id, student_info.major_id, student_info.dept_id,
                              student_info.class_id, student_info.student_name, student_info.sex, student_info.grade,
                              None, None, encrypted_str])])
        try:
            conn.execute(insert_query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_insert.post('/insert_staff', summary='insert staff')
def insert_staff(staff_info: UpdateInfoStaff):
    if staff_info.staff_id is None or staff_info.dept_id is None or staff_info.staff_name is None or \
            staff_info.sex is None or staff_info.date_of_birth is None or staff_info.ranks is None or \
            staff_info.salary is None:
        return {'msg': 'not enough information'}
    with Session(bind=engine) as conn:
        query = conn.query(Dept.dept_id).where(
            get_where_conditions(Dept.__table__.columns.values(), staff_info.dept_id, None))
        if len(query.all()) == 0:
            return {'msg': f'failed to insert, dept_id {staff_info.dept_id} does not exist.'}
        query = conn.query(Staff.staff_id).where(
            get_where_conditions(Staff.__table__.columns.values(), staff_info.staff_id, None, None, None, None,
                                 None, None))
        if len(query.all()) >= 1:
            return {'msg': f'failed to insert, staff_id {query.all()[0][0]} already exists.'}
        insert_query = insert(Staff).values(
            [get_update_dict(Staff.__table__.columns.keys(),
                             [staff_info.staff_id, staff_info.dept_id, staff_info.staff_name, staff_info.sex,
                              staff_info.date_of_birth, staff_info.ranks, staff_info.salary])])
        try:
            conn.execute(insert_query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_insert.post('/insert_all_course', summary='insert all course')
def insert_all_course(all_course_info: UpdateInfoAllCourse):
    if all_course_info.course_id is None or all_course_info.course_name is None or \
            all_course_info.credit is None or all_course_info.course_hours is None or \
            all_course_info.dept_id is None:
        return {'msg': 'not enough information'}
    with Session(bind=engine) as conn:
        query = conn.query(Dept.dept_id).where(
            get_where_conditions(Dept.__table__.columns.values(), all_course_info.dept_id, None))
        if len(query.all()) == 0:
            return {'msg': f'failed to insert, dept_id {all_course_info.dept_id} does not exist.'}
        query = conn.query(AllCourse.course_id).where(
            get_where_conditions(AllCourse.__table__.columns.values(), all_course_info.course_id,
                                 None, None, None, None))
        if len(query.all()) >= 1:
            return {'msg': f'failed to insert, course_id {query.all()[0][0]} already exists.'}
        insert_query = insert(AllCourse).values(
            [get_update_dict(AllCourse.__table__.columns.keys(),
                             [all_course_info.course_id, all_course_info.course_name, all_course_info.credit,
                              all_course_info.course_hours, all_course_info.dept_id])])
        try:
            conn.execute(insert_query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_insert.post('/insert_available_course', summary='insert available course')
def insert_available_course(available_course_info: UpdateInfoAvailableCourse):
    if available_course_info.course_id is None or available_course_info.semester is None or \
            available_course_info.staff_id is None or available_course_info.class_time is None or \
            available_course_info.class_place is None:
        return {'msg': 'not enough information'}
    with Session(bind=engine) as conn:
        query = conn.query(AllCourse.course_id).where(
            get_where_conditions(AllCourse.__table__.columns.values(), available_course_info.course_id))
        if len(query.all()) == 0:
            return {'msg': f'failed to insert, course_id {available_course_info.course_id} does not exist.'}
        query = conn.query(Staff.staff_id).where(
            get_where_conditions(Staff.__table__.columns.values(), available_course_info.staff_id))
        if len(query.all()) == 0:
            return {'msg': f'failed to insert, staff_id {available_course_info.staff_id} does not exist.'}
        query = conn.query(AvailableCourse.course_id, AvailableCourse.semester, AvailableCourse.staff_id,
                           AvailableCourse.class_time).where(
            get_where_conditions(AvailableCourse.__table__.columns.values(), available_course_info.course_id,
                                 available_course_info.semester, available_course_info.staff_id,
                                 available_course_info.class_time))
        if len(query.all()) >= 1:
            return {
                'msg': f'failed to insert, (course_id {query.all()[0][0]} semester {query.all()[0][1]} '
                       f'staff_id {query.all()[0][2]} class_time {query.all()[0][3]}) already exists.'}
        insert_query = insert(AvailableCourse).values(
            [get_update_dict(AvailableCourse.__table__.columns.keys(),
                             [available_course_info.course_id, available_course_info.semester,
                              available_course_info.staff_id, available_course_info.class_time,
                              available_course_info.class_place])])
        try:
            conn.execute(insert_query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_insert.post('/insert_selected_course_now', summary='insert selected course now')
def insert_selected_course_now(selected_course_now_info: UpdateInfoSelectedCourseNow):
    if selected_course_now_info.student_id is None or selected_course_now_info.semester is None or \
            selected_course_now_info.course_id is None or selected_course_now_info.staff_id is None or \
            selected_course_now_info.class_time is None:
        return {'msg': 'not enough information'}
    with Session(bind=engine) as conn:
        query = conn.query(Student.student_id).where(
            get_where_conditions(Student.__table__.columns.values(), selected_course_now_info.student_id))
        if len(query.all()) == 0:
            return {'msg': f'学生号 {selected_course_now_info.student_id} 不存在.'}
        query = conn.query(Staff.staff_id).where(
            get_where_conditions(Staff.__table__.columns.values(), selected_course_now_info.staff_id))
        if len(query.all()) == 0:
            return {'msg': f'教师号 {selected_course_now_info.staff_id} 不存在.'}
        query = conn.query(AvailableCourse.course_id, AvailableCourse.semester, AvailableCourse.staff_id,
                           AvailableCourse.class_time).where(
            get_where_conditions(AvailableCourse.__table__.columns.values(), selected_course_now_info.course_id,
                                 selected_course_now_info.semester, selected_course_now_info.staff_id,
                                 selected_course_now_info.class_time))
        if len(query.all()) == 0:
            return {
                'msg': f'本课程未开设'}
        query = conn.query(SelectedCourseNow.student_id, SelectedCourseNow.semester, SelectedCourseNow.course_id).where(
            get_where_conditions(SelectedCourseNow.__table__.columns.values(), selected_course_now_info.student_id,
                                 selected_course_now_info.semester, selected_course_now_info.course_id))
        if len(query.all()) >= 1:
            return {'msg': f'该学生已选该课'}

        insert_query = insert(SelectedCourseNow).values(
            [get_update_dict(SelectedCourseNow.__table__.columns.keys(),
                             [selected_course_now_info.student_id, selected_course_now_info.semester,
                              selected_course_now_info.course_id, selected_course_now_info.staff_id,
                              selected_course_now_info.class_time])])
        try:
            conn.execute(insert_query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}


@root_urls_insert.post('/insert_ended_course', summary='insert ended course')
def insert_ended_course(ended_course_info: UpdateInfoEndedCourse):
    if ended_course_info.student_id is None or ended_course_info.semester is None or ended_course_info.course_id is None \
            or ended_course_info.staff_id is None or ended_course_info.score_norm is None \
            or ended_course_info.score_test is None or ended_course_info.total_score is None:
        return {'msg': 'not enough information'}
    with Session(bind=engine) as conn:
        query = conn.query(Student.student_id).where(
            get_where_conditions(Student.__table__.columns.values(), ended_course_info.student_id))
        if len(query.all()) == 0:
            return {'msg': f'failed to insert, student_id {ended_course_info.student_id} does not exist.'}
        query = conn.query(Staff.staff_id).where(
            get_where_conditions(Staff.__table__.columns.values(), ended_course_info.staff_id))
        if len(query.all()) == 0:
            return {'msg': f'failed to insert, staff_id {ended_course_info.staff_id} does not exist.'}
        query = conn.query(AllCourse.course_id).where(
            get_where_conditions(AllCourse.__table__.columns.values(), ended_course_info.course_id))
        if len(query.all()) == 0:
            return {'msg': f'failed to insert, course_id {ended_course_info.course_id} does not exist.'}
        query = conn.query(EndedCourse.student_id, EndedCourse.semester, EndedCourse.course_id,
                           EndedCourse.staff_id).where(
            get_where_conditions(EndedCourse.__table__.columns.values(), ended_course_info.student_id,
                                 ended_course_info.semester, ended_course_info.course_id))
        if len(query.all()) >= 1:
            return {
                'msg': f'failed to insert, (student_id {ended_course_info.student_id}'
                       f' semester {ended_course_info.semester} course_id {ended_course_info.course_id}'
                       f' already exists.'}
        insert_query = insert(EndedCourse).values(
            [get_update_dict(EndedCourse.__table__.columns.keys(),
                             [ended_course_info.student_id, ended_course_info.semester, ended_course_info.course_id,
                              ended_course_info.staff_id, ended_course_info.score_norm, ended_course_info.score_test,
                              ended_course_info.total_score])])
        try:
            conn.execute(insert_query)
            conn.commit()
        except Exception as e:
            return {'msg': str(e)}
        return {'msg': 'success'}
