from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing import Union, List
from pydantic import BaseModel
from sqlalchemy import create_engine, text, insert, delete
from sqlalchemy.orm import Session
from database.models7 import *
from apps.tools import *
from sqlalchemy import and_
import re

student_urls = APIRouter()
engine = create_engine(url='mysql://root:' + SQL_PWD + '@localhost/my_school')


@student_urls.get('/search', summary='search course info(available_course)')
def search_course_info(cno: Union[str, None] = None, cname: Union[str, None] = None,
                       staff_id: Union[str, None] = None, staff_name: Union[str, None] = None):
    if cno is None and cname is None and staff_id is None and staff_name is None:
        return {'msg': 'not enough information.'}
    # search_dict = get_params_into_dict(cno=cno, cname=cname, staff_id=staff_id, staff_name=staff_name)
    with Session(bind=engine) as conn:
        query = conn.query(AvailableCourse.course_id, AllCourse.course_name,
                           AvailableCourse.semester, AvailableCourse.staff_id,
                           Staff.staff_name, AvailableCourse.class_time,
                           AvailableCourse.class_place).join(AllCourse,
                                                             AllCourse.course_id == AvailableCourse.course_id).join(
            Staff, Staff.staff_id == AvailableCourse.staff_id).where(
            get_where_conditions([AvailableCourse.course_id, AllCourse.course_name, AvailableCourse.staff_id,
                                  Staff.staff_name], cno, cname, staff_id, staff_name))
        ret_tuple_list = query.all()
        if len(ret_tuple_list) == 0:
            return {'msg': 'Course searched does not exist or is not available.'}
        ret_json = get_empty_json('course_id', 'course_name', 'semester', 'staff_id', 'staff_name', 'class_time',
                                  'class_place')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
        return ret_json


@student_urls.get('/get_schedule', summary='get schedule(selected_course_now)')
def get_schedule(sno: Union[str, None] = None):
    if sno is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Student.student_id).where(Student.student_id == sno)
        student_exists = query.all()
        if len(student_exists) == 0:
            return {'msg': 'Student does not exist.'}
        query = conn.query(SelectedCourseNow.course_id, AllCourse.course_name, SelectedCourseNow.semester,
                           SelectedCourseNow.staff_id, Staff.staff_name, SelectedCourseNow.class_time,
                           AvailableCourse.class_place) \
            .join(AvailableCourse,
                  and_(AvailableCourse.course_id == SelectedCourseNow.course_id, AvailableCourse.class_time ==
                       SelectedCourseNow.class_time)).join(
            AllCourse, AllCourse.course_id == SelectedCourseNow.course_id).join(Staff,
                                                                                Staff.staff_id == SelectedCourseNow.staff_id).where(
            SelectedCourseNow.student_id == sno)
        ret_tuple_list = query.all()
        ret_json = get_empty_json('course_id', 'course_name', 'semester', 'staff_id', 'staff_name', 'class_time',
                                  'class_place')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
        return ret_json


@student_urls.get('/get_finished', summary='get finished(ended_course)')
def get_finished(sno: Union[str, None] = None):
    if sno is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Student.student_id).where(Student.student_id == sno)
        student_exists = query.all()
        if len(student_exists) == 0:
            return {'msg': 'Student does not exist.'}
        query = conn.query(EndedCourse.course_id, AllCourse.course_name, EndedCourse.staff_id, Staff.staff_name,
                           EndedCourse.semester, EndedCourse.score_norm, EndedCourse.score_test,
                           EndedCourse.total_score, AllCourse.credit).join(AllCourse,
                                                                           AllCourse.course_id == EndedCourse.course_id).join(
            Staff, Staff.staff_id == EndedCourse.staff_id).where(
            EndedCourse.student_id == sno)
        ret_tuple_list = query.all()
        ret_json = get_empty_json('course_id', 'course_name', 'staff_id', 'staff_name', 'semester', 'score_norm',
                                  'score_test', 'total_score', 'credit')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
        return ret_json


@student_urls.get('/get_score', summary='get score(ended_course)')
def get_score(sno: Union[str, None] = None):
    if sno is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Student.student_id).where(Student.student_id == sno)
        student_exists = query.all()
        if len(student_exists) == 0:
            return {'msg': 'Student does not exist.'}
        query = conn.query(Student.gpa_total, Student.gpa_this).where(
            get_where_conditions(Student.__table__.columns.values(), sno))
    return {'gpa_this': query.all()[0][1], 'gpa_total': query.all()[0][0]}


@student_urls.get('/get_schedule_excel', summary='get schedule excel')
def download_schedule_excel(sno: Union[str, None] = None):
    if sno is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Student.student_id).where(Student.student_id == sno)
        student_exists = query.all()
        if len(student_exists) == 0:
            return {'msg': 'Student does not exist.'}
        query = conn.query(SelectedCourseNow.course_id, AllCourse.course_name, SelectedCourseNow.semester,
                           SelectedCourseNow.staff_id, Staff.staff_name, SelectedCourseNow.class_time,
                           AvailableCourse.class_place) \
            .join(AvailableCourse,
                  and_(AvailableCourse.course_id == SelectedCourseNow.course_id, AvailableCourse.class_time ==
                       SelectedCourseNow.class_time)).join(
            AllCourse, AllCourse.course_id == SelectedCourseNow.course_id).join(Staff,
                                                                                Staff.staff_id == SelectedCourseNow.staff_id).where(
            SelectedCourseNow.student_id == sno)
        ret_tuple_list = query.all()
        ret_json = get_empty_json('course_id', 'course_name', 'semester', 'staff_id', 'staff_name', 'class_time',
                                  'class_place')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
    course_names_list = ret_json['course_name']
    course_day_list = [item[0:2] for item in ret_json['class_time']]
    course_time_list = [item[2:] for item in ret_json['class_time']]
    df_schdule = pd.DataFrame(
        data={'时间': ['1-2节', '3-4节', '5-6节', '7-8节', '9-10节', '11-12节'],
              '周一': [None, None, None, None, None, None], '周二': [None, None, None, None, None, None],
              '周三': [None, None, None, None, None, None], '周四': [None, None, None, None, None, None],
              '周五': [None, None, None, None, None, None]})
    # df_schdule.set_index('time', inplace=True)
    dict_time2i = dict()
    for i, time in enumerate(df_schdule['时间']):
        dict_time2i[time] = i
    for cname, cday, ctime in zip(course_names_list, course_day_list, course_time_list):
        df_schdule.loc[dict_time2i[ctime], cday] = cname
    excel_content = generate_excel_content(data=df_schdule)
    return StreamingResponse(io.BytesIO(excel_content.read()),
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment;filename=schedule.xlsx"})


# @student_urls.get('/get_score/{mode}', summary='get score')
# def get_score(mode: str, sno: Union[str, None] = None, sms: Union[str, None] = None):
#     if sno is None:
#         return {}
#     with Session(bind=engine) as conn:
#         query = conn.query(Student.student_id).where(Student.student_id == sno)
#         student_exists = query.all()
#         if len(student_exists) == 0:
#             return {'msg': 'Student does not exist.'}
#     if mode == 'all':
#         with Session(bind=engine) as conn:
#             subquery = (
#                 select([
#                     func.sum(AllCourse.credit * EndedCourse.total_score) / func.sum(AllCourse.credit)
#                 ])
#                 .select_from(
#                     EndedCourse.__table__.join(AllCourse, EndedCourse.course_id == AllCourse.course_id)
#                     .join(Staff, Staff.staff_id == EndedCourse.staff_id)
#                 )
#                 .where(EndedCourse.student_id == sno)
#                 .group_by(EndedCourse.student_id)
#             )
#             avg_gpa = conn.query(subquery).scalar()
#             return {'sc': avg_gpa}
#     elif mode == 'this':
#         with Session(bind=engine) as conn:
#             query = conn.query(EndedCourse.course_id).where(EndedCourse.semester == sms)
#             semester_exists = query.all()
#             if len(semester_exists) == 0:
#                 return {'msg': 'Semester not recorded.'}
#         if sms is None:
#             return {}
#         with Session(bind=engine) as conn:
#             with Session(bind=engine) as conn:
#                 subquery = (
#                     select([
#                         func.sum(AllCourse.credit * EndedCourse.total_score) / func.sum(AllCourse.credit)
#                     ])
#                     .select_from(
#                         EndedCourse.__table__.join(AllCourse, EndedCourse.course_id == AllCourse.course_id)
#                         .join(Staff, Staff.staff_id == EndedCourse.staff_id)
#                     )
#                     .where(EndedCourse.student_id == sno)
#                     .where(EndedCourse.semester == sms)
#                     .group_by(EndedCourse.student_id)
#                 )
#                 avg_gpa = conn.query(subquery).scalar()
#                 return {'sc': avg_gpa}


class CourseInfo(BaseModel):
    course_id: Union[str, List[str], None] = None
    semester: Union[str, List[str], None] = None
    staff_id: Union[str, List[str], None] = None
    class_time: Union[str, List[str], None] = None


@student_urls.post('/insert_course', summary='insert course(change selected_course_now)')
def insert_course(course_info: CourseInfo, sno: Union[str, None] = None):
    if sno is None:
        return {'msg': '学生号不能为空'}
    with Session(bind=engine) as conn:
        query = conn.query(AvailableCourse.course_id).where(
            AvailableCourse.course_id == course_info.course_id and AvailableCourse.staff_id == course_info.staff_id
            and AvailableCourse.class_time == course_info.class_time)
        course_exist = query.all()
        if len(course_exist) == 0:
            return {'msg': '本学期未开设本课程'}
        query = conn.query(SelectedCourseNow.course_id).where(
            SelectedCourseNow.student_id == sno).where(SelectedCourseNow.course_id == course_info.course_id)
        course_selected = query.all()
        # print("!", len(course_selected), course_selected)
        if len(course_selected) > 0:
            return {'msg': '本课程已选'}
        query = conn.query(SelectedCourseNow.course_id).where(
            get_where_conditions(SelectedCourseNow.__table__.columns.values(), sno, None, None, None,
                                 course_info.class_time))
        time_conflict = query.all()
        if len(time_conflict) > 0:
            return {'msg': '课时冲突'}
        insert_query = insert(SelectedCourseNow).values(
            [{'student_id': sno, 'semester': course_info.semester, 'course_id': course_info.course_id,
              'staff_id': course_info.staff_id, 'class_time': course_info.class_time}])
        try:
            conn.execute(insert_query)
            conn.commit()
        except Exception as e:
            print(e)
            return {'msg': e}
    return {'msg': '选课成功'}


@student_urls.delete('/delete_course', summary='delete course(change selected_course_now)')
def delete_course(sno: Union[str, None] = None, semester: Union[str, None] = None,
                  course_id: Union[str, None] = None):
    if sno is None or semester is None or course_id is None:
        return {'msg': 'not enough information to delete.'}
    with Session(bind=engine) as conn:
        query = conn.query(SelectedCourseNow.course_id).where(SelectedCourseNow.student_id == sno).where(
            SelectedCourseNow.semester == semester).where(SelectedCourseNow.course_id == course_id)
        course_exist = query.all()
        if len(course_exist) == 0:
            return {'msg': 'fail to delete, course does not exist.'}
        delete_query = delete(SelectedCourseNow).where(SelectedCourseNow.student_id == sno).where(
            SelectedCourseNow.semester == semester).where(SelectedCourseNow.course_id == course_id)
        try:
            conn.execute(delete_query)
            conn.commit()
        except Exception as e:
            print(e)
            return {'msg': e}
    return {'msg': 'success'}
