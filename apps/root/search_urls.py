from fastapi import APIRouter
from sqlalchemy import create_engine, update, delete, insert
from sqlalchemy.orm import Session
from database.models6 import *
from apps.tools import *
from apps.root.updateinfo_root import *

root_urls_search = APIRouter()
engine = create_engine(url='mysql://root:' + SQL_PWD + '@localhost/my_school')


@root_urls_search.get('/search_dept', summary='search dept(dept)')
def search_dept(dept_id: Union[str, None] = None, dept_name: Union[str, None] = None):
    # if dept_id is None and dept_name is None:
    #     return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Dept.dept_id, Dept.dept_name).where(
            get_where_conditions(list(Dept.__table__.columns.values()), dept_id, dept_name))
        ret_tuple_list = query.all()
        if len(ret_tuple_list) == 0:
            return {'msg': 'Dept searched does not exist.'}
        ret_json = get_empty_json('dept_id', 'dept_name')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
        return ret_json


@root_urls_search.get('/search_major', summary='search major(major)')
def search_major(major_id: Union[str, None] = None, dept_id: Union[str, None] = None,
                 major_name: Union[str, None] = None):
    # if major_id is None and dept_id is None and major_name is None:
    #     return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Major.major_id, Major.dept_id, Major.major_name).where(
            get_where_conditions(list(Major.__table__.columns.values()), major_id, dept_id, major_name))
        ret_tuple_list = query.all()
        if len(ret_tuple_list) == 0:
            return {'msg': 'Major searched does not exist.'}
        ret_json = get_empty_json('major_id', 'dept_id', 'major_name')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
        return ret_json


@root_urls_search.get('/search_class', summary='search major(class)')
def search_class(class_id: Union[str, None] = None, dept_id: Union[str, None] = None,
                 major_id: Union[str, None] = None, class_name: Union[str, None] = None):
    # if class_id is None and dept_id is None and major_id is None and class_name is None:
    #     return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Clas.class_id, Clas.dept_id, Clas.major_id, Clas.class_name).where(
            get_where_conditions(list(Clas.__table__.columns.values()), class_id, dept_id, major_id, class_name))
        ret_tuple_list = query.all()
        if len(ret_tuple_list) == 0:
            return {'msg': 'Class searched does not exist.'}
        ret_json = get_empty_json('class_id', 'dept_id', 'major_id', 'class_name')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
        return ret_json


@root_urls_search.get('/search_student', summary='search student(student)')
def search_student(student_id: Union[str, None] = None, major_id: Union[str, None] = None,
                   dept_id: Union[str, None] = None, class_id: Union[str, None] = None,
                   student_name: Union[str, None] = None, sex: Union[str, None] = None, grade: Union[str, None] = None):
    # if student_id is None and major_id is None and \
    #         dept_id is None and class_id is None and student_name is None and sex is None:
    #     return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Student.student_id, Student.major_id, Student.dept_id, Student.class_id,
                           Student.student_name, Student.sex, Student.grade).where(
            get_where_conditions(list(Student.__table__.columns.values()), student_id, major_id, dept_id, class_id,
                                 student_name, sex, grade))
        ret_tuple_list = query.all()
        if len(ret_tuple_list) == 0:
            return {'msg': 'Student searched does not exist.'}
        ret_json = get_empty_json('student_id', 'major_id', 'dept_id', 'class_id',
                                  'student_name', 'sex', 'grade')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
        return ret_json


@root_urls_search.get('/search_staff', summary='search staff(staff)')
def search_staff(staff_id: Union[str, None] = None, dept_id: Union[str, None] = None,
                 staff_name: Union[str, None] = None, sex: Union[str, None] = None):
    # if staff_id is None and dept_id is None and staff_name is None and sex is None:
    #     return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Staff.staff_id, Staff.dept_id, Staff.staff_name,
                           Staff.sex, Staff.date_of_birth, Staff.ranks, Staff.salary).where(
            get_where_conditions(list(Staff.__table__.columns.values()), staff_id, dept_id, staff_name,
                                 sex, None, None, None))
        ret_tuple_list = query.all()
        if len(ret_tuple_list) == 0:
            return {'msg': 'Staff searched does not exist.'}
        ret_json = get_empty_json('staff_id', 'dept_id', 'staff_name',
                                  'sex', 'date_of_birth', 'ranks', 'salary')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
        return ret_json


@root_urls_search.get('/search_all_course', summary='search all course(all_course)')
def search_all_course(course_id: Union[str, None] = None, course_name: Union[str, None] = None,
                      dept_id: Union[str, None] = None):
    # if course_id is None and course_name is None and dept_id is None:
    #     return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(AllCourse.course_id, AllCourse.course_name, AllCourse.credit,
                           AllCourse.course_hours, AllCourse.dept_id).where(
            get_where_conditions(list(AllCourse.__table__.columns.values()), course_id, course_name,
                                 None, None, dept_id))
        ret_tuple_list = query.all()
        if len(ret_tuple_list) == 0:
            return {'msg': 'All course searched does not exist.'}
        ret_json = get_empty_json('course_id', 'course_name', 'credit', 'course_hours', 'dept_id')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
        return ret_json


@root_urls_search.get('/search_available_course', summary='search available course(available_course)')
def search_available_course(course_id: Union[str, None] = None, semester: Union[str, None] = None,
                            staff_id: Union[str, None] = None):
    # if course_id is None and semester is None and staff_id is None:
    #     return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(AvailableCourse.course_id, AvailableCourse.semester, AvailableCourse.staff_id,
                           AvailableCourse.class_time, AvailableCourse.class_place) \
            .where(
            get_where_conditions(list(AvailableCourse.__table__.columns.values()),
                                 course_id, semester, staff_id, None, None))
        ret_tuple_list = query.all()
        if len(ret_tuple_list) == 0:
            return {'msg': 'Available course searched does not exist.'}
        ret_json = get_empty_json('course_id', 'semester', 'staff_id', 'class_time', 'class_place')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
        return ret_json


@root_urls_search.get('/search_selected_course_now', summary='search selected course now(selected_course_now)')
def search_selected_course_now(student_id: Union[str, None] = None, course_id: Union[str, None] = None,
                               staff_id: Union[str, None] = None):
    # if course_id is None and semester is None and staff_id is None:
    #     return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(SelectedCourseNow.student_id, SelectedCourseNow.semester, SelectedCourseNow.course_id,
                           SelectedCourseNow.staff_id, SelectedCourseNow.class_time) \
            .where(
            get_where_conditions(list(SelectedCourseNow.__table__.columns.values()),
                                 student_id, None, course_id, staff_id, None))
        ret_tuple_list = query.all()
        if len(ret_tuple_list) == 0:
            return {'msg': 'Selected course searched does not exist.'}
        ret_json = get_empty_json('student_id', 'semester', 'course_id', 'staff_id', 'class_time')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
        return ret_json


@root_urls_search.get('/search_ended_course', summary='search ended course(ended_course)')
def search_ended_course(student_id: Union[str, None] = None, semester: Union[str, None] = None,
                        course_id: Union[str, None] = None, staff_id: Union[str, None] = None):
    # if course_id is None and semester is None and staff_id is None:
    #     return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(EndedCourse.student_id, EndedCourse.semester, EndedCourse.course_id, EndedCourse.staff_id,
                           EndedCourse.score_norm, EndedCourse.score_test, EndedCourse.total_score) \
            .where(
            get_where_conditions(list(EndedCourse.__table__.columns.values()),
                                 student_id, semester, course_id, staff_id, None, None, None))
        ret_tuple_list = query.all()
        if len(ret_tuple_list) == 0:
            return {'msg': 'Ended course searched does not exist.'}
        ret_json = get_empty_json('student_id', 'semester', 'course_id', 'staff_id', 'score_norm', 'score_test',
                                  'total_score')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
        return ret_json
