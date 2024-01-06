# coding: utf-8
from sqlalchemy import BigInteger, CHAR, CheckConstraint, Column, DateTime, Float, ForeignKey, ForeignKeyConstraint, \
    Index, Integer, String
from sqlalchemy.dialects.mysql import DATETIME, LONGTEXT, SMALLINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Dept(Base):
    __tablename__ = 'dept'

    dept_id = Column(CHAR(60), primary_key=True)
    dept_name = Column(CHAR(60), nullable=False)


class Major(Base):
    __tablename__ = 'major'

    major_id = Column(CHAR(60), primary_key=True)
    dept_id = Column(ForeignKey('dept.dept_id'), nullable=False, index=True)
    major_name = Column(CHAR(60), nullable=False)

    dept = relationship('Dept')


class Clas(Base):
    __tablename__ = 'class'

    class_id = Column(CHAR(60), primary_key=True)
    dept_id = Column(ForeignKey('dept.dept_id'), nullable=False, index=True)
    major_id = Column(ForeignKey('major.major_id'), nullable=False, index=True)
    class_name = Column(CHAR(60), nullable=False)

    dept = relationship('Dept')
    major = relationship('Major')


class Student(Base):
    __tablename__ = 'student'

    student_id = Column(CHAR(60), primary_key=True)
    major_id = Column(ForeignKey('major.major_id'), nullable=False, index=True)
    dept_id = Column(ForeignKey('dept.dept_id'), nullable=False, index=True)
    class_id = Column(ForeignKey('class.class_id'), nullable=False, index=True)
    student_name = Column(CHAR(60), nullable=False)
    sex = Column(CHAR(10), nullable=False)
    grade = Column(Integer, nullable=False)

    _class = relationship('Clas')
    dept = relationship('Dept')
    major = relationship('Major')


class Staff(Base):
    __tablename__ = 'staff'

    staff_id = Column(CHAR(60), primary_key=True)
    dept_id = Column(ForeignKey('dept.dept_id'), nullable=False, index=True)
    staff_name = Column(CHAR(60), nullable=False)
    sex = Column(CHAR(10), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    ranks = Column(CHAR(60), nullable=False)
    salary = Column(Float, nullable=False)

    dept = relationship('Dept')


class AllCourse(Base):
    __tablename__ = 'all_course'

    course_id = Column(CHAR(60), primary_key=True)
    course_name = Column(CHAR(60), nullable=False)
    credit = Column(Integer, nullable=False)
    course_hours = Column(Integer, nullable=False)
    dept_id = Column(ForeignKey('dept.dept_id'), nullable=False, index=True)

    dept = relationship('Dept')


class AvailableCourse(Base):
    __tablename__ = 'available_course'

    course_id = Column(ForeignKey('all_course.course_id'), primary_key=True, nullable=False, index=True)
    semester = Column(CHAR(60), primary_key=True, nullable=False)
    staff_id = Column(ForeignKey('staff.staff_id'), primary_key=True, nullable=False, index=True)
    class_time = Column(CHAR(60), primary_key=True, nullable=False)
    class_place = Column(CHAR(60), nullable=False)

    course = relationship('AllCourse')
    staff = relationship('Staff')


class EndedCourse(Base):
    __tablename__ = 'ended_course'

    student_id = Column(ForeignKey('student.student_id'), primary_key=True, nullable=False, index=True)
    semester = Column(CHAR(60), primary_key=True, nullable=False)
    course_id = Column(ForeignKey('all_course.course_id'), primary_key=True, nullable=False, index=True)
    staff_id = Column(ForeignKey('staff.staff_id'), nullable=False, index=True)
    score_norm = Column(Float)
    score_test = Column(Float)
    total_score = Column(Float)

    course = relationship('AllCourse')
    staff = relationship('Staff')
    student = relationship('Student')


class SelectedCourseNow(Base):
    __tablename__ = 'selected_course_now'
    __table_args__ = (
        ForeignKeyConstraint(['course_id', 'semester', 'staff_id', 'class_time'],
                             ['available_course.course_id', 'available_course.semester', 'available_course.staff_id',
                              'available_course.class_time']),
        Index('course_id', 'course_id', 'semester', 'staff_id', 'class_time')
    )

    student_id = Column(ForeignKey('student.student_id'), primary_key=True, nullable=False, index=True)
    semester = Column(CHAR(60), primary_key=True, nullable=False)
    course_id = Column(CHAR(60), primary_key=True, nullable=False, index=True)
    staff_id = Column(ForeignKey('staff.staff_id'), nullable=False, index=True)
    class_time = Column(CHAR(60), nullable=False)

    course = relationship('AvailableCourse')
    staff = relationship('Staff')
    student = relationship('Student')


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True)


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DATETIME(fsp=6))
    is_superuser = Column(TINYINT(1), nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(TINYINT(1), nullable=False)
    is_active = Column(TINYINT(1), nullable=False)
    date_joined = Column(DATETIME(fsp=6), nullable=False)


class DjangoContentType(Base):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        Index('django_content_type_app_label_model_76bd3d3b_uniq', 'app_label', 'model', unique=True),
    )

    id = Column(Integer, primary_key=True)
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)


class DjangoMigration(Base):
    __tablename__ = 'django_migrations'

    id = Column(BigInteger, primary_key=True)
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DATETIME(fsp=6), nullable=False)


class DjangoSession(Base):
    __tablename__ = 'django_session'

    session_key = Column(String(40), primary_key=True)
    session_data = Column(LONGTEXT, nullable=False)
    expire_date = Column(DATETIME(fsp=6), nullable=False, index=True)


class AuthPermission(Base):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        Index('auth_permission_content_type_id_codename_01ab375a_uniq', 'content_type_id', 'codename', unique=True),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    content_type_id = Column(ForeignKey('django_content_type.id'), nullable=False)
    codename = Column(String(100), nullable=False)

    content_type = relationship('DjangoContentType')


class AuthUserGroup(Base):
    __tablename__ = 'auth_user_groups'
    __table_args__ = (
        Index('auth_user_groups_user_id_group_id_94350c0c_uniq', 'user_id', 'group_id', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False, index=True)

    group = relationship('AuthGroup')
    user = relationship('AuthUser')


class DjangoAdminLog(Base):
    __tablename__ = 'django_admin_log'
    __table_args__ = (
        CheckConstraint('(`action_flag` >= 0)'),
    )

    id = Column(Integer, primary_key=True)
    action_time = Column(DATETIME(fsp=6), nullable=False)
    object_id = Column(LONGTEXT)
    object_repr = Column(String(200), nullable=False)
    action_flag = Column(SMALLINT, nullable=False)
    change_message = Column(LONGTEXT, nullable=False)
    content_type_id = Column(ForeignKey('django_content_type.id'), index=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False, index=True)

    content_type = relationship('DjangoContentType')
    user = relationship('AuthUser')


class AuthGroupPermission(Base):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        Index('auth_group_permissions_group_id_permission_id_0cd325b0_uniq', 'group_id', 'permission_id', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    group = relationship('AuthGroup')
    permission = relationship('AuthPermission')


class AuthUserUserPermission(Base):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        Index('auth_user_user_permissions_user_id_permission_id_14a6b632_uniq', 'user_id', 'permission_id',
              unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    permission = relationship('AuthPermission')
    user = relationship('AuthUser')

