from pydantic import BaseModel
from typing import Union


class UpdateInfoDept(BaseModel):
    dept_id: Union[str, None] = None
    dept_name: Union[str, None] = None


class UpdateInfoMajor(BaseModel):
    major_id: Union[str, None] = None
    dept_id: Union[str, None] = None
    major_name: Union[str, None] = None


class UpdateInfoClass(BaseModel):
    class_id: Union[str, None] = None
    dept_id: Union[str, None] = None
    major_id: Union[str, None] = None
    class_name: Union[str, None] = None


class UpdateInfoStudent(BaseModel):
    student_id: Union[str, None] = None
    major_id: Union[str, None] = None
    dept_id: Union[str, None] = None
    class_id: Union[str, None] = None
    student_name: Union[str, None] = None
    sex: Union[str, None] = None
    grade: Union[int, None] = None
    pwd: Union[str, None] = None


class UpdateInfoStaff(BaseModel):
    staff_id: Union[str, None] = None
    dept_id: Union[str, None] = None
    staff_name: Union[str, None] = None
    sex: Union[str, None] = None
    date_of_birth: Union[str, None] = None
    ranks: Union[str, None] = None
    salary: Union[float, None] = None


class UpdateInfoAllCourse(BaseModel):
    course_id: Union[str, None] = None
    course_name: Union[str, None] = None
    credit: Union[int, None] = None
    course_hours: Union[int, None] = None
    dept_id: Union[str, None] = None


class UpdateInfoAvailableCourse(BaseModel):
    course_id: Union[str, None] = None
    semester: Union[str, None] = None
    staff_id: Union[str, None] = None
    class_time: Union[str, None] = None
    class_place: Union[str, None] = None


class UpdateInfoSelectedCourseNow(BaseModel):
    student_id: Union[str, None] = None
    semester: Union[str, None] = None
    course_id: Union[str, None] = None
    staff_id: Union[str, None] = None
    class_time: Union[str, None] = None


class UpdateInfoEndedCourse(BaseModel):
    student_id: Union[str, None] = None
    semester: Union[str, None] = None
    course_id: Union[str, None] = None
    credit_record: Union[int, None] = None
    staff_id: Union[str, None] = None
    score_norm: Union[float, None] = None
    score_test: Union[float, None] = None
    total_score: Union[float, None] = None
