# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Dept(Base):
    __tablename__ = 'dept'

    dept_id = Column(CHAR(60), primary_key=True)
    dept_name = Column(CHAR(60), nullable=False)


class EndedCourse(Base):
    __tablename__ = 'ended_course'

    student_id = Column(CHAR(60), primary_key=True, nullable=False, index=True)
    semester = Column(CHAR(60), primary_key=True, nullable=False)
    course_id = Column(CHAR(60), primary_key=True, nullable=False, index=True)
    staff_id = Column(CHAR(60), nullable=False, index=True)
    score_norm = Column(Float)
    score_test = Column(Float)
    total_score = Column(Float)


class SelectedCourseNow(Base):
    __tablename__ = 'selected_course_now'

    student_id = Column(CHAR(60), primary_key=True, nullable=False, index=True)
    semester = Column(CHAR(60), primary_key=True, nullable=False)
    course_id = Column(CHAR(60), primary_key=True, nullable=False, index=True)
    staff_id = Column(CHAR(60), nullable=False)
    class_time = Column(CHAR(60), nullable=False)


class AllCourse(Base):
    __tablename__ = 'all_course'

    course_id = Column(CHAR(60), primary_key=True)
    course_name = Column(CHAR(60), nullable=False)
    credit = Column(Integer, nullable=False)
    course_hours = Column(Integer, nullable=False)
    dept_id = Column(ForeignKey('dept.dept_id', onupdate='CASCADE'), nullable=False, index=True)

    dept = relationship('Dept')


class Major(Base):
    __tablename__ = 'major'

    major_id = Column(CHAR(60), primary_key=True)
    dept_id = Column(ForeignKey('dept.dept_id', onupdate='CASCADE'), nullable=False, index=True)
    major_name = Column(CHAR(60), nullable=False)

    dept = relationship('Dept')


class Staff(Base):
    __tablename__ = 'staff'

    staff_id = Column(CHAR(60), primary_key=True)
    dept_id = Column(ForeignKey('dept.dept_id', onupdate='CASCADE'), nullable=False, index=True)
    staff_name = Column(CHAR(60), nullable=False)
    sex = Column(CHAR(10), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    ranks = Column(CHAR(60), nullable=False)
    salary = Column(Float, nullable=False)

    dept = relationship('Dept')


class AvailableCourse(Base):
    __tablename__ = 'available_course'

    course_id = Column(ForeignKey('all_course.course_id', onupdate='CASCADE'), primary_key=True, nullable=False,
                       index=True)
    semester = Column(CHAR(60), primary_key=True, nullable=False)
    staff_id = Column(ForeignKey('staff.staff_id', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    class_time = Column(CHAR(60), primary_key=True, nullable=False)
    class_place = Column(CHAR(60), nullable=False)

    course = relationship('AllCourse')
    staff = relationship('Staff')


class Clas(Base):
    __tablename__ = 'class'

    class_id = Column(CHAR(60), primary_key=True)
    dept_id = Column(ForeignKey('dept.dept_id', onupdate='CASCADE'), nullable=False, index=True)
    major_id = Column(ForeignKey('major.major_id', onupdate='CASCADE'), nullable=False, index=True)
    class_name = Column(CHAR(60), nullable=False)

    dept = relationship('Dept')
    major = relationship('Major')


class Student(Base):
    __tablename__ = 'student'

    student_id = Column(CHAR(60), primary_key=True)
    major_id = Column(ForeignKey('major.major_id', onupdate='CASCADE'), nullable=False, index=True)
    dept_id = Column(ForeignKey('dept.dept_id', onupdate='CASCADE'), nullable=False, index=True)
    class_id = Column(ForeignKey('class.class_id', onupdate='CASCADE'), nullable=False, index=True)
    student_name = Column(CHAR(60), nullable=False)
    sex = Column(CHAR(10), nullable=False)
    grade = Column(Integer, nullable=False)

    _class = relationship('Clas')
    dept = relationship('Dept')
    major = relationship('Major')
