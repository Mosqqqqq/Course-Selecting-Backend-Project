from fastapi import APIRouter
from typing import Union, List
from pydantic import BaseModel
from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session
from database.models7 import *
from apps.tools import *

staff_urls = APIRouter()
engine = create_engine(url='mysql://root:' + SQL_PWD + '@localhost/my_school')


@staff_urls.get('/search_course_finished', summary='search finished course(ended_course)')
def search_course_finished(staff_id: Union[str, None] = None):
    if staff_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Staff.staff_name).where(Staff.staff_id == staff_id)
        staff_exists = query.all()
        if len(staff_exists) == 0:
            return {'msg': 'staff does not exists.'}
        query = conn.query(EndedCourse.semester, EndedCourse.course_id, AllCourse.course_name, AllCourse.credit,
                           AllCourse.course_hours).join(AllCourse, AllCourse.course_id == EndedCourse.course_id).where(
            EndedCourse.staff_id == staff_id).distinct()
        ret_tuple_list = query.all()
        if len(ret_tuple_list) == 0:
            return {'msg': 'course finished does not exist.'}
        ret_json = get_empty_json('semester', 'course_id', 'course_name', 'credit', 'course_hours')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
        return ret_json


@staff_urls.get('/search_course_open_this semester', summary='search course open for this semester(available_course)')
def search_course_this_semester(staff_id: Union[str, None] = None):
    if staff_id is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(Staff.staff_name).where(Staff.staff_id == staff_id)
        staff_exists = query.all()
        if len(staff_exists) == 0:
            return {'msg': 'staff does not exists.'}
        query = conn.query(AvailableCourse.semester, AvailableCourse.course_id, AllCourse.course_name, AllCourse.credit,
                           AllCourse.course_hours, AvailableCourse.class_time, AvailableCourse.class_place).join(
            AllCourse, AllCourse.course_id == AvailableCourse.course_id).where(
            AvailableCourse.staff_id == staff_id)
        ret_tuple_list = query.all()
        ret_json = get_empty_json('semester', 'course_id', 'course_name', 'credit', 'course_hours', 'class_time',
                                  'class_place')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
        return ret_json


@staff_urls.get('/search_name_list_for_course', summary='search name list for course(selected_course_now)')
def search_name_list(staff_id: Union[str, None] = None, course_id: Union[str, None] = None,
                     class_time: Union[str, None] = None):
    if staff_id is None or course_id is None or class_time is None:
        return {'msg': 'not enough information.'}
    with Session(bind=engine) as conn:
        query = conn.query(SelectedCourseNow.student_id, Student.student_name) \
            .join(Student, SelectedCourseNow.student_id == Student.student_id) \
            .where(SelectedCourseNow.staff_id == staff_id) \
            .where(SelectedCourseNow.course_id == course_id) \
            .where(SelectedCourseNow.class_time == class_time)
        ret_tuple_list = query.all()
        ret_json = get_empty_json('student_id', 'student_name')
        for tup in ret_tuple_list:
            for item, key in zip(tup, ret_json.keys()):
                ret_json[key].append(item)
        return ret_json


class ScoreInfo(BaseModel):
    student_id: Union[str, List[str], None] = None
    semester: Union[str, List[str], None] = None
    course_id: Union[str, List[str], None] = None
    norm_score: Union[str, List[str], None] = None
    test_score: Union[str, List[str], None] = None
    total_score: Union[str, List[str], None] = None


@staff_urls.post('/give_score', summary='give score to student(change ended_course)')
def give_score(score_info: ScoreInfo, staff_id: Union[str, None] = None):
    if score_info.student_id is None or score_info.semester is None or score_info.course_id is None:
        return {'msg': 'not enough information.'}
    elif type(score_info.student_id) == str:
        with Session(bind=engine) as conn:
            query = conn.query(EndedCourse.student_id) \
                .where(EndedCourse.student_id == score_info.student_id) \
                .where(EndedCourse.semester == score_info.semester) \
                .where(EndedCourse.course_id == score_info.course_id)
            if len(query.all()) >= 1:
                # 分数已经登过，只需要修改
                query = update(EndedCourse).where(EndedCourse.student_id == score_info.student_id) \
                    .where(EndedCourse.semester == score_info.semester) \
                    .where(EndedCourse.course_id == score_info.course_id).values(score_norm=score_info.norm_score,
                                                                                 score_test=score_info.test_score,
                                                                                 total_score=score_info.total_score)
                try:
                    conn.execute(query)
                    conn.commit()
                except Exception as e:
                    return {'msg': str(e)}
                return {'msg': 'update success.'}
            elif len(query.all()) == 0:
                # 分数未登过
                new_record = EndedCourse(student_id=score_info.student_id, semester=score_info.semester,
                                         course_id=score_info.course_id, staff_id=staff_id,
                                         score_norm=float(score_info.norm_score),
                                         score_test=float(score_info.test_score),
                                         total_score=float(score_info.total_score)
                                         )
                try:
                    conn.add(new_record)
                    conn.commit()
                except Exception as e:
                    return {'msg': str(e)}
                return {'msg': 'insert and update success.'}
    elif type(score_info.student_id) == list:
        response_json = {'msgs': []}
        for sno, sms, cno, norm_score, test_score, total_score in zip(score_info.student_id, score_info.semester,
                                                                      score_info.course_id,
                                                                      score_info.norm_score, score_info.test_score,
                                                                      score_info.total_score):
            with Session(bind=engine) as conn:
                query = conn.query(EndedCourse.student_id) \
                    .where(EndedCourse.student_id == sno) \
                    .where(EndedCourse.semester == sms) \
                    .where(EndedCourse.course_id == cno)
                if len(query.all()) >= 1:
                    # 分数已经登过，只需要修改
                    query = update(EndedCourse).where(EndedCourse.student_id == sno) \
                        .where(EndedCourse.semester == sms) \
                        .where(EndedCourse.course_id == cno).values(score_norm=test_score,
                                                                    score_test=test_score,
                                                                    total_score=total_score)
                    try:
                        conn.execute(query)
                        conn.commit()
                    except Exception as e:
                        return {'msg': str(e)}
                    response_json['msgs'].append('update success.')
                elif len(query.all()) == 0:
                    # 分数未登过
                    new_record = EndedCourse(student_id=sno, semester=sms,
                                             course_id=cno, staff_id=staff_id,
                                             score_norm=float(norm_score),
                                             score_test=float(test_score),
                                             total_score=float(total_score)
                                             )
                    try:
                        conn.add(new_record)
                        conn.commit()
                    except Exception as e:
                        return {'msg': str(e)}
                    response_json['msgs'].append('insert and update success.')
        return response_json
    else:
        return {'msg': 'received wrong request json.'}

