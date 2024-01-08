drop database my_school;
create database my_school;
use my_school;
create table dept
(
	dept_id char(60) not null,
	dept_name char(60) not null,
	primary key(dept_id)
);

create table major
(
	major_id char(60) not null,
	dept_id char(60) not null,
	major_name char(60) not null,
	primary key(major_id),
	foreign key(dept_id) references dept(dept_id) on update cascade on delete cascade
);
-- 班级（隶属于专业）
create table class
(
	class_id char(60) not null,
	dept_id char(60) not null,
	major_id char(60) not null,
	class_name char(60) not null,
	primary key(class_id),
	foreign key(dept_id) references dept(dept_id) on update cascade on delete cascade,
	foreign key(major_id) references major(major_id) on update cascade on delete cascade
);
-- 学生（隶属于班级）
create table student
(
	student_id char(60) not null,
	major_id char(60) not null,
	dept_id char(60) not null,
	class_id char(60) not null,
	student_name char(60) not null,
	sex char(10) not null,
	grade int not null,
    gpa_this float default null,
    gpa_total float default null,
    pwd text not null,
	primary key(student_id),
	foreign key(major_id) references major(major_id) on update cascade on delete cascade,
	foreign key(dept_id) references dept(dept_id) on update cascade on delete cascade,
	foreign key(class_id) references class(class_id) on update cascade on delete cascade
);
-- 教职工（隶属于部门）
create table staff
(
	staff_id char(60) not null,
	dept_id char(60) not null,
	staff_name char(60) not null,
	sex char(10) not null,
	date_of_birth datetime not null,
	ranks char(60) not null,
	salary float not null,
    pwd text not null,
	primary key(staff_id),
	foreign key(dept_id) references dept(dept_id) on update cascade on delete cascade
);

-- 学校可以开设的全部课程（隶属于部门）
create table all_course
(
	course_id char(60) not null,
	course_name char(60) not null,
	credit int not null,
	course_hours int not null,
	dept_id char(60) not null,
	primary key(course_id),
	foreign key(dept_id) references dept(dept_id) on update cascade on delete cascade
);

-- 本学期可选的课（隶属于学校可以开设的全部课程）
-- semester是最新学期
create table available_course
(
	course_id char(60) not null,
	semester char(60) not null,
	staff_id char(60) not null,
	class_time char(60) not null,
	class_place char(60) not null,
	primary key(course_id, semester, staff_id, class_time),
	foreign key(course_id) references all_course(course_id) on update cascade on delete cascade,
	foreign key(staff_id) references staff(staff_id) on update cascade on delete cascade
);

-- 本学期的选课记录
create table selected_course_now
(
	student_id char(60) not null,
	semester char(60) not null,
	course_id char(60) not null,
	staff_id char(60) not null,
	class_time char(60) not null,	-- 此处冗余的class_time用于做外键
	primary key(student_id, semester, course_id),
    foreign key(student_id) references student(student_id) on update cascade on delete cascade,
	foreign key(staff_id) references staff(staff_id) on update cascade on delete cascade
    -- foreign key(course_id, semester, staff_id, class_time) references available_course(course_id, semester, staff_id, class_time) on update cascade on delete cascade
);

-- foreign key(student_id) references student(student_id) on update cascade
-- create trigger update_student_selected_course_now
-- after update on student
-- for each row
-- update selected_course_now
-- set student_id = new.student_id
-- where student_id = old.student_id;

-- create trigger delete_student_selected_course_now
-- after delete on student
-- for each row
-- delete from selected_course_now
-- where student_id = old.student_id;

-- DELIMITER //
-- CREATE TRIGGER check_student_id_before_insert
-- BEFORE INSERT ON selected_course_now
-- FOR EACH ROW
-- BEGIN
--     DECLARE student_count INT;
--     SELECT COUNT(*) INTO student_count FROM student WHERE student_id = NEW.student_id;
--     
--     IF student_count = 0 THEN
--         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: student_id does not exist in the student table';
--     END IF;
-- END //
-- DELIMITER ;

-- DELIMITER //
-- CREATE TRIGGER check_student_id_before_update
-- BEFORE UPDATE ON selected_course_now
-- FOR EACH ROW
-- BEGIN
--     DECLARE student_count INT;
--     SELECT COUNT(*) INTO student_count FROM student WHERE student_id = NEW.student_id;
--     
--     IF student_count = 0 THEN
--         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: New student_id does not exist in the student table';
--         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Rolling back update due to invalid student_id';
--     END IF;
-- END //
-- DELIMITER ;




-- 	foreign key(staff_id) references staff(staff_id) on update cascade,
-- create trigger update_staff_selected_course_now
-- after update on staff
-- for each row
-- update selected_course_now
-- set staff_id = new.staff_id
-- where staff_id = old.staff_id;

-- create trigger delete_staff_selected_course_now
-- after delete on staff
-- for each row
-- delete from selected_course_now
-- where staff_id = old.staff_id;

-- DELIMITER //
-- CREATE TRIGGER check_staff_id_before_insert
-- BEFORE INSERT ON selected_course_now
-- FOR EACH ROW
-- BEGIN
--     DECLARE staff_count INT;
--     SELECT COUNT(*) INTO staff_count FROM staff WHERE staff_id = NEW.staff_id;
--     
--     IF staff_count = 0 THEN
--         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: staff_id does not exist in the staff table';
--     END IF;
-- END //
-- DELIMITER ;

-- DELIMITER //
-- CREATE TRIGGER check_staff_id_before_update
-- BEFORE UPDATE ON selected_course_now
-- FOR EACH ROW
-- BEGIN
--     DECLARE staff_count INT;
--     SELECT COUNT(*) INTO staff_count FROM staff WHERE staff_id = NEW.staff_id;
--     
--     IF staff_count = 0 THEN
--         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: New staff_id does not exist in the staff table';
--         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Rolling back update due to invalid staff_id';
--     END IF;
-- END //
-- DELIMITER ;

-- 	foreign key(course_id, semester, staff_id, class_time) references available_course(course_id, semester, staff_id, class_time) on update cascade
create trigger update_available_course_selected_course_now
after update on available_course
for each row
update selected_course_now
set course_id = new.course_id, semester = new.semester, staff_id = new.staff_id, class_time = new.class_time
where course_id = old.course_id and semester = old.semester and staff_id = old.staff_id and class_time = old.class_time;

create trigger delete_available_course_selected_course_now
after delete on available_course
for each row
delete from selected_course_now
where course_id = old.course_id and semester = old.semester and staff_id = old.staff_id and class_time = old.class_time;

DELIMITER //
CREATE TRIGGER check_available_course_before_insert
BEFORE INSERT ON selected_course_now
FOR EACH ROW
BEGIN
    DECLARE available_course_count INT;
    SELECT COUNT(*) INTO available_course_count
    FROM available_course
    WHERE course_id = NEW.course_id and semester = new.semester and staff_id = new.staff_id and class_time = new.class_time;
    IF available_course_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: available_course does not exist in the available_course table';
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER check_available_course_before_update
BEFORE update ON selected_course_now
FOR EACH ROW
BEGIN
    DECLARE available_course_count INT;
    SELECT COUNT(*) INTO available_course_count
    FROM available_course
    WHERE course_id = NEW.course_id and semester = new.semester and staff_id = new.staff_id and class_time = new.class_time;
    IF available_course_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: available_course does not exist in the available_course table';
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Rolling back update';
    END IF;
END //
DELIMITER ;

-- 已结课的选课记录
create table ended_course
(
	student_id char(60) not null,
	semester char(60) not null,
	course_id char(60) not null,
	staff_id char(60) not null,
	score_norm float,
	score_test float,
	total_score float,
	primary key(student_id, semester, course_id),
	foreign key(student_id) references student(student_id) on update cascade on delete no action,
	foreign key(staff_id) references staff(staff_id) on update cascade on delete no action,
	foreign key(course_id) references all_course(course_id) on update cascade on delete no action
);

-- create trigger update_student_ended_course
-- after UPDATE ON student
-- FOR EACH ROW
-- UPDATE ended_course
-- SET student_id = NEW.student_id
-- WHERE student_id = OLD.student_id;

-- create trigger update_staff_ended_course
-- after UPDATE ON staff
-- FOR EACH ROW
-- UPDATE ended_course
-- SET staff_id = NEW.staff_id
-- WHERE staff_id = OLD.staff_id;

-- create trigger update_all_course_ended_course
-- after UPDATE ON all_course
-- FOR EACH ROW
-- UPDATE ended_course
-- SET course_id = NEW.course_id
-- WHERE course_id = OLD.course_id;

create index idx_major_dept_id on major (dept_id);

create index idx_class_dept_id on class (dept_id);
create index idx_class_major_id on class (major_id);

create index idx_student_major_id on student (major_id);
create index idx_student_dept_id on student (dept_id);
create index idx_student_class_id on student (class_id);

create index idx_staff_dept_id on staff (dept_id);

create index idx_all_course_dept_id on all_course (dept_id);

create index idx_available_course_course_id on available_course (course_id);
create index idx_available_course_staff_id on available_course (staff_id);

create index idx_selected_course_now_student_id on selected_course_now (student_id);
create index idx_selected_course_now_course_id on selected_course_now (course_id);

create index idx_ended_course_student_id on ended_course (student_id);
create index idx_ended_course_course_id on ended_course (course_id);
create index idx_ended_course_staff_id on ended_course (staff_id);

INSERT INTO dept (dept_id, dept_name) VALUES
('D001', '计算机工程与科学学院'),
('D002', '电气工程学院'),
('D003', '数学与统计学院'),
('D004', '外国语学院'),
('D005', '法学院'),
('D006', '社会学院'),
('D007', '新闻传播学院'),
('D008', '文化遗产与信息管理学院'),
('D009', '经济学院'),
('D010', '管理学院'),
('D011', '悉尼工商学院'),
('D012', '上海美术学院'),
('D013', '上海电影学院'),
('D014', '音乐学院'),
('D015', '上海温哥华电影学院'),
('D016', '钱伟长学院'),
('D017', '理学院'),
('D018', '通信与信息工程学院（翔英学院）'),
('D019', '机电工程与自动化学院'),
('D020', '材料科学与工程学院'),
('D021', '环境与化学工程学院'),
('D022', '生命科学学院'),
('D023', '中欧工程技术学院');

INSERT INTO major (major_id, dept_id, major_name) VALUES
-- 计算机学院
('M001', 'D001', '计算机科学与技术'),
('M002', 'D001', '软件工程'),
('M003', 'D001', '网络工程'),

-- 电气工程学院
('M004', 'D002', '电气工程与自动化'),
('M005', 'D002', '电子信息工程'),
('M006', 'D002', '智能电网技术'),

-- 数学与统计学院
('M007', 'D003', '数学与应用数学'),
('M008', 'D003', '统计学'),

-- 外国语学院
('M009', 'D004', '英语'),
('M010', 'D004', '法语'),

-- 法学院
('M011', 'D005', '法学'),
('M012', 'D005', '国际法'),

-- 社会学院
('M013', 'D006', '社会学'),
('M014', 'D006', '社会工作'),

-- 新闻传播学院
('M015', 'D007', '新闻学'),
('M016', 'D007', '广告学'),

-- 文化遗产与信息管理学院
('M017', 'D008', '文化遗产保护与利用'),
('M018', 'D008', '信息管理与信息系统'),

-- 经济学院
('M019', 'D009', '经济学'),
('M020', 'D009', '金融学'),

-- 管理学院
('M021', 'D010', '工商管理'),
('M022', 'D010', '人力资源管理'),

-- 悉尼工商学院
('M023', 'D011', '国际贸易'),
('M024', 'D011', '市场营销'),

-- 上海美术学院
('M025', 'D012', '美术学'),
('M026', 'D012', '设计学'),

-- 上海电影学院
('M027', 'D013', '电影制作'),
('M028', 'D013', '影视编导'),

-- 音乐学院
('M029', 'D014', '音乐学'),
('M030', 'D014', '舞蹈表演'),

-- 上海温哥华电影学院
('M031', 'D015', '电影艺术'),
('M032', 'D015', '数字媒体技术'),

-- 钱伟长学院
('M033', 'D016', '艺术设计'),
('M034', 'D016', '视觉传达设计'),

-- 理学院
('M035', 'D017', '数学'),
('M036', 'D017', '物理学'),

-- 通信与信息工程学院（翔英学院）
('M037', 'D018', '通信工程'),
('M038', 'D018', '信息工程'),


-- 机电工程与自动化学院
('M041', 'D019', '机械工程'),
('M042', 'D019', '自动化'),

-- 材料科学与工程学院
('M043', 'D020', '材料科学与工程'),
('M044', 'D020', '新能源材料'),

-- 环境与化学工程学院
('M045', 'D021', '环境工程'),
('M046', 'D021', '化学工程'),

-- 生命科学学院
('M047', 'D022', '生物科学'),
('M048', 'D022', '生物技术'),

-- 中欧工程技术学院
('M049', 'D023', '电气工程与自动化'),
('M050', 'D023', '工程管理');
INSERT INTO class (class_id, dept_id, major_id, class_name) VALUES
-- 计算机科学与技术
('CL001', 'D001', 'M001', '计算机科学与技术1班'),
('CL002', 'D001', 'M001', '计算机科学与技术2班'),
-- 软件工程
('CL003', 'D001', 'M002', '软件工程1班'),
-- 网络工程
('CL004', 'D001', 'M003', '网络工程1班'),
-- 电气工程与自动化
('CL005', 'D002', 'M004', '电气工程与自动化1班'),
-- 电子信息工程
('CL006', 'D002', 'M005', '电子信息工程1班'),
-- 智能电网技术
('CL007', 'D002', 'M006', '智能电网技术1班'),
-- 数学与应用数学
('CL008', 'D003', 'M007', '数学与应用数学1班'),
-- 统计学
('CL009', 'D003', 'M008', '统计学1班'),
-- 英语
('CL010', 'D004', 'M009', '英语1班'),
-- 法语
('CL011', 'D004', 'M010', '法语1班'),
-- 法学
('CL012', 'D005', 'M011', '法学1班'),
-- 国际法
('CL013', 'D005', 'M012', '国际法1班'),
-- 社会学
('CL014', 'D006', 'M013', '社会学1班'),
-- 社会工作
('CL015', 'D006', 'M014', '社会工作1班'),
-- 新闻学
('CL016', 'D007', 'M015', '新闻学1班'),
-- 广告学
('CL017', 'D007', 'M016', '广告学1班'),
-- 文化遗产保护与利用
('CL018', 'D008', 'M017', '文化遗产保护与利用1班'),
-- 信息管理与信息系统
('CL019', 'D008', 'M018', '信息管理与信息系统1班'),
-- 经济学
('CL020', 'D009', 'M019', '经济学1班'),
-- 金融学
('CL021', 'D009', 'M020', '金融学1班'),
-- 工商管理
('CL022', 'D010', 'M021', '工商管理1班'),
-- 人力资源管理
('CL023', 'D010', 'M022', '人力资源管理1班'),
-- 国际贸易
('CL024', 'D011', 'M023', '国际贸易1班'),
-- 市场营销
('CL025', 'D011', 'M024', '市场营销1班'),
-- 美术学
('CL026', 'D012', 'M025', '美术学1班'),
-- 设计学
('CL027', 'D012', 'M026', '设计学1班'),
-- 电影制作
('CL028', 'D013', 'M027', '电影制作1班'),
-- 影视编导
('CL029', 'D013', 'M028', '影视编导1班'),
-- 音乐学
('CL030', 'D014', 'M029', '音乐学1班'),
-- 舞蹈表演
('CL031', 'D014', 'M030', '舞蹈表演1班'),
-- 电影艺术
('CL032', 'D015', 'M031', '电影艺术1班'),
-- 数字媒体技术
('CL033', 'D015', 'M032', '数字媒体技术1班'),
-- 艺术设计
('CL034', 'D016', 'M033', '艺术设计1班'),
-- 视觉传达设计
('CL035', 'D016', 'M034', '视觉传达设计1班'),
-- 数学
('CL036', 'D017', 'M035', '数学1班'),
-- 物理学
('CL037', 'D017', 'M036', '物理学1班'),
-- 通信工程
('CL038', 'D018', 'M037', '通信工程1班'),
-- 信息工程
('CL039', 'D018', 'M038', '信息工程1班'),
-- 机械工程
('CL040', 'D019', 'M041', '机械工程1班'),
-- 自动化
('CL041', 'D019', 'M042', '自动化1班'),
-- 材料科学与工程
('CL042', 'D020', 'M043', '材料科学与工程1班'),
-- 新能源材料
('CL043', 'D020', 'M044', '新能源材料1班'),
-- 环境工程
('CL044', 'D021', 'M045', '环境工程1班'),
-- 化学工程
('CL045', 'D021', 'M046', '化学工程1班'),
-- 生物科学
('CL046', 'D022', 'M047', '生物科学1班'),
-- 生物技术
('CL047', 'D022', 'M048', '生物技术1班'),
-- 电气工程与自动化（中欧工程技术学院）
('CL048', 'D023', 'M049', '电气工程与自动化1班'),
-- 工程管理（中欧工程技术学院）
('CL049', 'D023', 'M050', '工程管理1班');
INSERT INTO all_course (course_id, course_name, credit, course_hours, dept_id) VALUES
-- 计算机学院
('CS101', '计算机基础', 3, 48, 'D001'),
('CS102', '数据结构', 4, 64, 'D001'),
('CS103', '数据库设计', 3, 48, 'D001'),

-- 电气工程学院
('EE101', '电路分析', 3, 48, 'D002'),
('EE102', '信号与系统', 4, 64, 'D002'),
('EE103', '电力系统分析', 3, 48, 'D002'),

-- 数学与统计学院
('MA101', '高等数学', 4, 64, 'D003'),
('MA102', '概率论与数理统计', 3, 48, 'D003'),
('MA103', '线性代数', 3, 48, 'D003'),

-- 外国语学院
('FL101', '英语写作', 3, 48, 'D004'),
('FL102', '法语口语', 2, 32, 'D004'),

-- 法学院
('LW101', '宪法学', 3, 48, 'D005'),
('LW102', '合同法', 3, 48, 'D005'),
('LW103', '刑法学', 4, 64, 'D005'),

-- 社会学院
('SO101', '社会学导论', 3, 48, 'D006'),
('SO102', '社会调查方法', 4, 64, 'D006'),

-- 新闻传播学院
('CM101', '大众传播原理', 3, 48, 'D007'),
('CM102', '新闻写作与编辑', 4, 64, 'D007'),

-- 文化遗产与信息管理学院
('CH101', '文物学', 3, 48, 'D008'),
('IM101', '信息管理原理', 4, 64, 'D008'),

-- 经济学院
('EC101', '微观经济学', 3, 48, 'D009'),
('EC102', '宏观经济学', 4, 64, 'D009'),

-- 管理学院
('MG101', '管理学原理', 3, 48, 'D010'),
('MG102', '市场营销', 4, 64, 'D010'),

-- 悉尼工商学院
('IB101', '国际贸易概论', 3, 48, 'D011'),
('IB102', '国际市场营销', 4, 64, 'D011'),

-- 上海美术学院
('FA101', '西方美术史', 3, 48, 'D012'),
('FA102', '素描与速写', 2, 32, 'D012'),

-- 上海电影学院
('FM101', '电影导论', 3, 48, 'D013'),
('FM102', '剧本写作', 4, 64, 'D013'),

-- 音乐学院
('MU101', '音乐理论基础', 3, 48, 'D014'),
('MU102', '声乐技巧', 2, 32, 'D014'),

-- 上海温哥华电影学院
('VF101', '视觉传达基础', 3, 48, 'D015'),
('VF102', '数字媒体制作', 4, 64, 'D015'),

-- 钱伟长学院
('AD101', '艺术设计原理', 3, 48, 'D016'),
('AD102', '平面设计', 2, 32, 'D016'),

-- 理学院
('MA201', '数学分析', 4, 64, 'D017'),
('PH201', '经典力学', 4, 64, 'D017'),

-- 通信与信息工程学院（翔英学院）
('TE101', '通信原理', 3, 48, 'D018'),
('TE102', '数字信号处理', 4, 64, 'D018'),

-- 机电工程与自动化学院
('ME101', '工程制图', 3, 48, 'D019'),
('ME102', '自动控制原理', 4, 64, 'D019'),

-- 材料科学与工程学院
('MS101', '材料力学', 3, 48, 'D020'),
('MS102', '材料物理与化学', 4, 64, 'D020'),

-- 环境与化学工程学院
('EN101', '环境化学', 3, 48, 'D021'),
('EN102', '化工原理', 4, 64, 'D021'),

-- 生命科学学院
('BI101', '生物化学', 3, 48, 'D022'),
('BI102', '分子生物学', 4, 64, 'D022'),

-- 中欧工程技术学院
('CE101', '电气工程基础', 3, 48, 'D023'),
('CE102', '工程管理概论', 4, 64, 'D023'),
('CS104', '计算机网络', 3, 48, 'D001'),
('CS105', '软件工程实践', 2, 32, 'D001'),
-- 电气工程学院
('EE104', '数字信号处理', 3, 48, 'D002'),
('EE105', '电力电子技术', 2, 32, 'D002'),
('MA104', '数学建模', 3, 48, 'D003'),
('MA105', '统计分析', 2, 32, 'D003'),
-- 外国语学院
('FL103', '英美文学导读', 3, 48, 'D004'),
('FL104', '法语文学欣赏', 2, 32, 'D004'),
-- 法学院
('LW104', '刑法实例分析', 3, 48, 'D005'),
('LW105', '国际私法', 2, 32, 'D005'),
-- 社会学院
('SO103', '社会调查案例分析', 3, 48, 'D006'),
('SO104', '社会心理学', 2, 32, 'D006'),
-- 新闻传播学院
('CM103', '新闻摄影与摄像', 3, 48, 'D007'),
('CM104', '传播学理论', 2, 32, 'D007'),
-- 文化遗产与信息管理学院
('CH102', '文物保护技术', 3, 48, 'D008'),
('IM102', '信息系统设计', 2, 32, 'D008'),
-- 经济学院
('EC103', '产业经济学', 3, 48, 'D009'),
('EC104', '金融市场与投资', 2, 32, 'D009'),
-- 管理学院
('MG103', '组织行为学', 3, 48, 'D010'),
('MG104', '战略管理', 2, 32, 'D010'),
-- 悉尼工商学院
('IB103', '跨文化管理', 3, 48, 'D011'),
('IB104', '国际商务法', 2, 32, 'D011'),
-- 上海美术学院
('FA103', '西方艺术理论', 3, 48, 'D012'),
('FA104', '创意设计实践', 2, 32, 'D012'),
-- 上海电影学院
('FM103', '影视剧本创作', 3, 48, 'D013'),
('FM104', '电影艺术理论', 2, 32, 'D013'),
-- 音乐学院
('MU103', '音乐欣赏', 3, 48, 'D014'),
('MU104', '舞台演出技巧', 2, 32, 'D014'),
-- 上海温哥华电影学院
('VF103', '数字媒体艺术实践', 3, 48, 'D015'),
('VF104', '影视后期制作', 2, 32, 'D015'),
-- 钱伟长学院
('AD103', '数字艺术设计', 3, 48, 'D016'),
('AD104', '广告文案策划', 2, 32, 'D016'),
-- 理学院
('MA202', '复变函数', 4, 64, 'D017'),
('PH202', '电磁学', 4, 64, 'D017'),
-- 通信与信息工程学院（翔英学院）
('TE103', '移动通信技术', 3, 48, 'D018'),
('TE104', '网络安全原理', 2, 32, 'D018'),
-- 机电工程与自动化学院
('ME103', '机械设计基础', 3, 48, 'D019'),
('ME104', '自动控制系统设计', 2, 32, 'D019'),
-- 材料科学与工程学院
('MS103', '材料制备工艺', 3, 48, 'D020'),
('MS104', '新材料开发', 2, 32, 'D020'),
-- 环境与化学工程学院
('EN103', '环境影响评价', 3, 48, 'D021'),
('EN104', '化工过程控制', 2, 32, 'D021'),
-- 生命科学学院
('BI103', '生态学基础', 3, 48, 'D022'),
('BI104', '遗传学导论', 2, 32, 'D022'),
-- 中欧工程技术学院
('CE103', '电气工程设计', 3, 48, 'D023'),
('CE104', '工程项目管理', 2, 32, 'D023');
INSERT INTO student (student_id, major_id, dept_id, class_id, student_name, sex, grade, pwd)
VALUES
('S001', 'M001', 'D001', 'CL001', '张三', '男', 2, ''),
('S002', 'M002', 'D001', 'CL002', '李四', '女', 3, ''),
('S003', 'M003', 'D001', 'CL003', '王五', '男', 4, ''),
('S004', 'M001', 'D001', 'CL001', '赵六', '女', 1, ''),
('S005', 'M002', 'D001', 'CL002', '钱七', '男', 4, ''),
('S1001', 'M023', 'D011', 'CL021', '孙二十七', '男', 2, ''),
('S1002', 'M024', 'D011', 'CL022', '李二十八', '女', 4, ''),
('S101', 'M004', 'D002', 'CL003', '吴九', '男', 2, ''),
('S102', 'M005', 'D002', 'CL004', '周十', '女', 2, ''),
('S1101', 'M025', 'D012', 'CL023', '周二十九', '男', 3, ''),
('S1102', 'M026', 'D012', 'CL024', '吴三十', '女', 4, ''),
('S1201', 'M027', 'D013', 'CL025', '郑三十一', '男', 3, ''),
('S1202', 'M028', 'D013', 'CL026', '王三十二', '女', 2, ''),
('S1301', 'M029', 'D014', 'CL027', '陈三十三', '男', 4, ''),
('S1302', 'M030', 'D014', 'CL028', '杨三十四', '女', 3, ''),
('S1401', 'M031', 'D015', 'CL029', '赵三十五', '男', 1, ''),
('S1402', 'M032', 'D015', 'CL030', '孙三十六', '女', 3, ''),
('S1501', 'M033', 'D016', 'CL031', '李三十七', '男', 2, ''),
('S1502', 'M034', 'D016', 'CL032', '周三十八', '女', 3, ''),
('S1601', 'M035', 'D017', 'CL033', '吴三十九', '男', 2, ''),
('S1602', 'M036', 'D017', 'CL034', '许四十', '女', 3, ''),
('S1701', 'M037', 'D018', 'CL035', '李四十一', '男', 4, ''),
('S1702', 'M038', 'D018', 'CL036', '周四十二', '女', 3, ''),
('S1801', 'M041', 'D019', 'CL037', '吴四十三', '男', 4, ''),
('S1802', 'M042', 'D019', 'CL038', '许四十四', '女', 1, ''),
('S1901', 'M043', 'D020', 'CL039', '严四十五', '男', 4, ''),
('S1902', 'M044', 'D020', 'CL040', '胡四十六', '女', 3, ''),
('S2001', 'M045', 'D021', 'CL041', '潘四十七', '男', 4, ''),
('S2002', 'M046', 'D021', 'CL042', '曹四十八', '女', 3, ''),
('S201', 'M007', 'D003', 'CL005', '许十一', '男', 4, ''),
('S202', 'M008', 'D003', 'CL006', '严十二', '女', 3, ''),
('S2101', 'M047', 'D022', 'CL043', '朱四十九', '男', 2, ''),
('S2102', 'M048', 'D022', 'CL044', '李五十', '女', 4, ''),
('S2201', 'M049', 'D023', 'CL045', '赵五十一', '男', 3, ''),
('S2202', 'M050', 'D023', 'CL046', '钱五十二', '女', 4, ''),
('S301', 'M009', 'D004', 'CL007', '钟十三', '男', 4, ''),
('S302', 'M010', 'D004', 'CL008', '陆十四', '女', 3, ''),
('S401', 'M011', 'D005', 'CL009', '胡十五', '男', 1, ''),
('S402', 'M012', 'D005', 'CL010', '潘十六', '女', 1, ''),
('S501', 'M013', 'D006', 'CL011', '朱十七', '男', 1, ''),
('S502', 'M014', 'D006', 'CL012', '曹十八', '女', 1, ''),
('S601', 'M015', 'D007', 'CL013', '吕十九', '男', 4, ''),
('S602', 'M016', 'D007', 'CL014', '任二十', '女', 3, ''),
('S701', 'M017', 'D008', 'CL015', '韩二十一', '男', 4, ''),
('S702', 'M018', 'D008', 'CL016', '杜二十二', '女', 1, ''),
('S801', 'M019', 'D009', 'CL017', '陆二十三', '男', 1, ''),
('S802', 'M020', 'D009', 'CL018', '彭二十四', '女', 1, ''),
('S901', 'M021', 'D010', 'CL019', '赵二十五', '男', 4, ''),
('S902', 'M022', 'D010', 'CL020', '钱二十六', '女', 1, '');
INSERT INTO staff (staff_id, dept_id, staff_name, sex, date_of_birth, ranks, salary, pwd) VALUES
('ST101', 'D001', '张老师', '男', '1975-05-15', '教授', 8000.00, ''),
('ST102', 'D001', '王老师', '女', '1980-08-22', '副教授', 7000.00, ''),
('ST103', 'D002', '李老师', '男', '1982-11-18', '教授', 8200.00, ''),
('ST104', 'D002', '赵老师', '女', '1985-02-25', '讲师', 6500.00, ''),
('ST105', 'D003', '钱老师', '男', '1978-04-12', '副教授', 7500.00, ''),
('ST106', 'D003', '孙老师', '女', '1981-07-30', '助理教授', 6800.00, ''),
('ST107', 'D004', '周老师', '男', '1976-09-08', '教授', 8100.00, ''),
('ST108', 'D004', '吴老师', '女', '1979-12-14', '副教授', 7200.00, ''),
('ST109', 'D005', '郑老师', '男', '1983-01-20', '教授', 8300.00, ''),
('ST110', 'D005', '王老师', '女', '1986-04-28', '讲师', 6600.00, ''),
('ST111', 'D006', '冯老师', '男', '1977-06-01', '副教授', 7400.00, ''),
('ST112', 'D006', '陈老师', '女', '1982-08-17', '教授', 8100.00, ''),
('ST113', 'D007', '卫老师', '男', '1979-10-23', '讲师', 6700.00, ''),
('ST114', 'D007', '朱老师', '女', '1984-01-30', '助理教授', 6900.00, ''),
('ST115', 'D008', '秦老师', '男', '1974-02-10', '教授', 8200.00, ''),
('ST116', 'D008', '尤老师', '女', '1977-05-18', '副教授', 7300.00, ''),
('ST117', 'D009', '许老师', '男', '1980-07-25', '讲师', 6600.00, ''),
('ST118', 'D009', '何老师', '女', '1983-10-31', '教授', 8100.00, ''),
('ST119', 'D010', '吕老师', '男', '1985-01-05', '副教授', 7200.00, ''),
('ST120', 'D010', '张老师', '女', '1988-04-13', '教授', 8300.00, ''),
('ST121', 'D011', '谢老师', '男', '1976-06-20', '助理教授', 6800.00, ''),
('ST122', 'D011', '孟老师', '女', '1979-09-28', '讲师', 6500.00, ''),
('ST123', 'D012', '沈老师', '男', '1982-12-04', '教授', 8000.00, ''),
('ST124', 'D012', '徐老师', '女', '1985-03-12', '副教授', 7100.00, ''),
('ST125', 'D013', '林老师', '男', '1988-05-18', '讲师', 6700.00, ''),
('ST126', 'D013', '方老师', '女', '1991-08-26', '教授', 8200.00, ''),
('ST127', 'D014', '苏老师', '男', '1974-09-01', '副教授', 7300.00, ''),
('ST128', 'D014', '胡老师', '女', '1977-12-09', '助理教授', 6900.00, ''),
('ST129', 'D015', '陈老师', '男', '1980-02-15', '教授', 8100.00, ''),
('ST130', 'D015', '许老师', '女', '1983-05-23', '副教授', 7200.00, ''),
('ST131', 'D016', '赵老师', '男', '1986-08-30', '讲师', 6600.00, ''),
('ST132', 'D016', '杨老师', '女', '1989-12-07', '教授', 8300.00, ''),
('ST133', 'D017', '徐老师', '男', '1975-01-14', '副教授', 7400.00, ''),
('ST134', 'D017', '何老师', '女', '1978-04-24', '助理教授', 6700.00, ''),
('ST135', 'D018', '尹老师', '男', '1981-07-31', '教授', 8100.00, ''),
('ST136', 'D018', '丁老师', '女', '1984-11-07', '讲师', 6500.00, ''),
('ST137', 'D019', '范老师', '男', '1977-01-20', '副教授', 7200.00, ''),
('ST138', 'D019', '谢老师', '女', '1980-04-28', '教授', 8300.00, ''),
('ST139', 'D020', '黄老师', '男', '1983-07-12', '讲师', 6800.00, ''),
('ST140', 'D020', '曹老师', '女', '1986-10-20', '副教授', 7100.00, ''),
('ST141', 'D021', '董老师', '男', '1978-02-01', '教授', 8000.00, ''),
('ST142', 'D021', '万老师', '女', '1981-05-09', '讲师', 6700.00, ''),
('ST143', 'D022', '马老师', '男', '1984-08-16', '副教授', 7400.00, ''),
('ST144', 'D022', '孔老师', '女', '1987-11-23', '教授', 8100.00, ''),
('ST145', 'D023', '顾老师', '男', '1976-01-30', '讲师', 6600.00, ''),
('ST146', 'D023', '梁老师', '女', '1979-05-08', '助理教授', 6900.00, '');
INSERT INTO available_course (course_id, semester, staff_id, class_time, class_place)
VALUES
-- 计算机工程与科学学院
('CS101', '2023Spring', 'ST101', '周一1-2节', '教01-0101'),
('CS102', '2023Spring', 'ST102', '周三3-4节', '教01-0102'),

-- 电气工程学院
('EE101', '2023Spring', 'ST103', '周二5-6节', '教02-0201'),
('EE102', '2023Spring', 'ST104', '周四7-8节', '教02-0202'),

-- 数学与统计学院
('MA101', '2023Spring', 'ST105', '周一9-10节', '教03-0301'),
('MA102', '2023Spring', 'ST106', '周三11-12节', '教03-0302'),

-- 外国语学院
('FL101', '2023Spring', 'ST107', '周二13-14节', '教04-0401'),
('FL102', '2023Spring', 'ST108', '周四15-16节', '教04-0402'),

-- 法学院
('LW101', '2023Spring', 'ST109', '周一17-18节', '教05-0501'),
('LW102', '2023Spring', 'ST110', '周三19-20节', '教05-0502'),

-- 社会学院
('SO101', '2023Spring', 'ST111', '周二21-22节', '教06-0601'),
('SO102', '2023Spring', 'ST112', '周四23-24节', '教06-0602'),

-- 新闻传播学院
('CM101', '2023Spring', 'ST113', '周一25-26节', '教07-0701'),
('CM102', '2023Spring', 'ST114', '周三27-28节', '教07-0702'),

-- 文化遗产与信息管理学院
('CH102', '2023Spring', 'ST115', '周二29-30节', '教08-0801'),
('IM102', '2023Spring', 'ST116', '周四31-32节', '教08-0802'),

-- 经济学院
('EC101', '2023Spring', 'ST117', '周一33-34节', '教09-0901'),
('EC102', '2023Spring', 'ST118', '周三35-36节', '教09-0902'),

-- 管理学院
('MG101', '2023Spring', 'ST119', '周二37-38节', '教10-1001'),
('MG102', '2023Spring', 'ST120', '周四39-40节', '教10-1002'),

-- 悉尼工商学院
('IB101', '2023Spring', 'ST121', '周一41-42节', '教11-1101'),
('IB102', '2023Spring', 'ST122', '周三43-44节', '教11-1102'),

-- 上海美术学院
('FA101', '2023Spring', 'ST123', '周二45-46节', '教12-1201'),
('FA102', '2023Spring', 'ST124', '周四1-2节', '教12-1202'),

-- 上海电影学院
('FM101', '2023Spring', 'ST125', '周一3-4节', '教13-1301'),
('FM102', '2023Spring', 'ST126', '周三5-6节', '教13-1302'),

('MU101', '2023Spring', 'ST127', '周一1-2节', '音乐厅'),
('MU102', '2023Spring', 'ST128', '周三3-4节', '音乐厅'),
('VF101', '2023Spring', 'ST129', '周二5-6节', '影视厅'),
('VF102', '2023Spring', 'ST130', '周四7-8节', '影视厅'),
('AD101', '2023Spring', 'ST131', '周一9-10节', '艺术厅'),
('AD102', '2023Spring', 'ST132', '周三11-12节', '艺术厅'),
('MA201', '2023Spring', 'ST133', '周二13-14节', '实验室'),
('PH201', '2023Spring', 'ST134', '周四15-16节', '实验室'),
('TE101', '2023Spring', 'ST135', '周一17-18节', '教学楼A101'),
('TE102', '2023Spring', 'ST136', '周三19-20节', '教学楼A102'),
('ME101', '2023Spring', 'ST137', '周二21-22节', '实验室'),
('ME102', '2023Spring', 'ST138', '周四23-24节', '实验室'),
('MS101', '2023Spring', 'ST139', '周一25-26节', '实验室'),
('MS102', '2023Spring', 'ST140', '周三27-28节', '实验室'),
('EN101', '2023Spring', 'ST141', '周二29-30节', '教学楼B101'),
('EN102', '2023Spring', 'ST142', '周四31-32节', '教学楼B102'),
('BI101', '2023Spring', 'ST143', '周一33-34节', '实验室'),
('BI102', '2023Spring', 'ST144', '周三35-36节', '实验室'),
('CE101', '2023Spring', 'ST145', '周二37-38节', '实验室'),
('CE102', '2023Spring', 'ST146', '周四39-40节', '实验室');
INSERT INTO selected_course_now (student_id, semester, course_id, staff_id, class_time) VALUES
('S001', '2023Spring', 'AD101', 'ST131', '周一9-10节'),
('S002', '2023Spring', 'AD102', 'ST132', '周三11-12节'),
('S003', '2023Spring', 'BI101', 'ST143', '周一33-34节'),
('S004', '2023Spring', 'BI102', 'ST144', '周三35-36节'),
('S005', '2023Spring', 'CE101', 'ST145', '周二37-38节'),
('S101', '2023Spring', 'CE102', 'ST146', '周四39-40节'), -- 修正学生号
('S102', '2023Spring', 'CH102', 'ST115', '周二29-30节'), -- 修正学生号
('S201', '2023Spring', 'EN101', 'ST141', '周二29-30节'), -- 修正学生号
('S202', '2023Spring', 'EN102', 'ST142', '周四31-32节');

INSERT INTO ended_course(student_id, semester, course_id, staff_id, score_norm, score_test, total_score) VALUES
('S001', '2022Autumn', 'CS101', 'ST101', 85, 90, 88.5),
('S001', '2022Autumn', 'MA101', 'ST105', 92, 88, 89),
('S001', '2022Autumn', 'EN101', 'ST141', 78, 82, 81),
('S001', '2022Autumn', 'PH201', 'ST134', 75, 88, 84),
('S001', '2022Autumn', 'BI101', 'ST143', 90, 78, 82),
('S001', '2022Autumn', 'FL101', 'ST107', 85, 92, 90),
('S002', '2022Autumn', 'PH201', 'ST134', 75, 88, 84),
('S002', '2022Autumn', 'BI101', 'ST143', 90, 78, 82),
('S002', '2022Autumn', 'FL101', 'ST107', 85, 92, 90)
;

DELIMITER //
-- CREATE PROCEDURE cal_gpa()
-- BEGIN
--     update student
--     set gpa_total = (
-- 		select
-- 		sum(credit * total_score) / sum(credit)
-- 		from ended_course
-- 		inner join all_course on all_course.course_id = ended_course.course_id
-- 		inner join staff on staff.staff_id = ended_course.staff_id
-- 		where ended_course.student_id = student_id
-- 	);
--     
--     update student
--     set gpa_this = (
-- 		select
-- 		sum(credit * total_score) / sum(credit)
-- 		from ended_course
-- 		inner join all_course on all_course.course_id = ended_course.course_id
-- 		inner join staff on staff.staff_id = ended_course.staff_id
-- 		where ended_course.student_id = student_id
--         and ended_course.semester in (
-- 			select semester
--             from selected_course_now
--         )
-- 	);
-- END //


CREATE PROCEDURE cal_gpa()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE student_id_value CHAR(60);
    
    -- Declare cursor for student_id
    DECLARE cur CURSOR FOR SELECT DISTINCT student_id FROM student;

    -- Declare continue handler for not found
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN cur;

    -- Loop to process each student_id
    main_loop: LOOP
        -- Fetch the next student_id
        FETCH cur INTO student_id_value;
        
        -- Exit the loop if no more rows
        IF done THEN
            LEAVE main_loop;
        END IF;

        -- Update gpa_total for the current student_id
        UPDATE student
        SET gpa_total = (
            SELECT SUM(credit * total_score) / SUM(credit)
            FROM ended_course
            INNER JOIN all_course ON all_course.course_id = ended_course.course_id
            INNER JOIN staff ON staff.staff_id = ended_course.staff_id
            WHERE ended_course.student_id = student_id_value
        )
        WHERE student_id = student_id_value;

        -- Update gpa_this for the current student_id
        UPDATE student
        SET gpa_this = (
            SELECT SUM(credit * total_score) / SUM(credit)
            FROM ended_course
            INNER JOIN all_course ON all_course.course_id = ended_course.course_id
            INNER JOIN staff ON staff.staff_id = ended_course.staff_id
            WHERE ended_course.student_id = student_id_value
            AND ended_course.semester IN (
                SELECT semester
                FROM selected_course_now
            )
        )
        WHERE student_id = student_id_value;
    END LOOP;

    -- Close the cursor
    CLOSE cur;
END //
DELIMITER ;

SET SQL_SAFE_UPDATES = 0;
call cal_gpa();
SET SQL_SAFE_UPDATES = 1;