-- Active: 1718680968425@@127.0.0.1@3306@lab
DROP TABLE IF EXISTS Score;

DROP TABLE IF EXISTS PPDate;
DROP TABLE IF EXISTS PrizePunish;


DROP TABLE IF EXISTS Admin;
DROP TABLE IF EXISTS Stupassword;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Student;
CREATE TABLE Student
(
    Sno CHAR(9) PRIMARY KEY,
    Sname VARCHAR(20) NOT NULL,
    Ssex CHAR(2) NOT NULL,
    Sdept VARCHAR(20) NOT NULL,
    Spic VARCHAR(20)
);

CREATE TABLE Course
(
    Cid CHAR(4) PRIMARY KEY,
    Cname VARCHAR(20) NOT NULL,
    Credit INT NOT NULL
);

CREATE TABLE Score
(
Sno CHAR(9) NOT NULL,
Cid CHAR(4) NOT NULL,
Score INT,
PRIMARY KEY (Sno, Cid),
CONSTRAINT fk_Score_Sno FOREIGN KEY (Sno) REFERENCES Student(Sno),
CONSTRAINT fk_Score_Cid FOREIGN KEY (Cid) REFERENCES Course(Cid)
);

CREATE TABLE PrizePunish
(
    PPid CHAR(4) PRIMARY KEY,
    PPContent VARCHAR(100) NOT NULL
);

CREATE TABLE PPDate
(
    Sno CHAR(9) NOT NULL,
    PPid CHAR(4) NOT NULL,
    Date DATE NOT NULL,
    PRIMARY KEY (Sno, PPid),
    CONSTRAINT fk_PPDate_Sno FOREIGN KEY (Sno) REFERENCES Student(Sno),
    CONSTRAINT fk_PPDate_PPid FOREIGN KEY (PPid) REFERENCES PrizePunish(PPid)
);


CREATE TABLE Admin
(
    name CHAR(9) PRIMARY KEY,
    password VARCHAR(20) NOT NULL
);

CREATE TABLE Stupassword
(
    Sno CHAR(9) PRIMARY KEY,
    password VARCHAR(20) NOT NULL,
    CONSTRAINT fk_Stupassword_Sno FOREIGN KEY (Sno) REFERENCES Student(Sno)
);

-- Insert sample data into Student table
INSERT INTO Student (Sno, Sname, Ssex, Sdept, Spic) VALUES ('202100001', 'Alice', 'F', 'CS', '1.jpg');
INSERT INTO Student (Sno, Sname, Ssex, Sdept, Spic) VALUES ('202100002', 'Bob', 'M', 'MATH', '2.jpg');
INSERT INTO Student (Sno, Sname, Ssex, Sdept, Spic) VALUES ('202100003', 'Charlie', 'M', 'PHY', '3.jpg');

-- Insert sample data into Course table
INSERT INTO Course (Cid, Cname, Credit) VALUES ('C001', 'Mathematics', 4);
INSERT INTO Course (Cid, Cname, Credit) VALUES ('C002', 'Physics', 3);
INSERT INTO Course (Cid, Cname, Credit) VALUES ('C003', 'Chemistry', 3);

-- Insert sample data into Score table
INSERT INTO Score (Sno, Cid, Score) VALUES ('202100001', 'C001', 85);
INSERT INTO Score (Sno, Cid, Score) VALUES ('202100001', 'C002', 90);
INSERT INTO Score (Sno, Cid, Score) VALUES ('202100002', 'C001', 78);
INSERT INTO Score (Sno, Cid, Score) VALUES ('202100002', 'C003', 82);
INSERT INTO Score (Sno, Cid, Score) VALUES ('202100003', 'C002', 92);
INSERT INTO Score (Sno, Cid, Score) VALUES ('202100003', 'C003', 88);

-- Insert sample data into PrizePunish table
INSERT INTO PrizePunish (PPid, PPContent) VALUES ('P001', 'Excellent performance in Mathematics');
INSERT INTO PrizePunish (PPid, PPContent) VALUES ('P002', 'Violation of academic integrity');

-- Insert sample data into PPDate table
INSERT INTO PPDate (Sno, PPid, Date) VALUES ('202100001', 'P001', '2021-09-01');
INSERT INTO PPDate (Sno, PPid, Date) VALUES ('202100002', 'P002', '2021-10-15');
INSERT INTO PPDate (Sno, PPid, Date) VALUES ('202100003', 'P001', '2021-11-30');

INSERT INTO admin(name, password) VALUES ('admin', 'admin');

INSERT INTO Stupassword(Sno, password) VALUES ('202100001', '123456');
INSERT INTO Stupassword(Sno, password) VALUES ('202100002', '123456');
INSERT INTO Stupassword(Sno, password) VALUES ('202100003', '123456');

DROP PROCEDURE IF EXISTS updateSno;
DROP PROCEDURE IF EXISTS updateCid;


# 存储过程：更新学号
#新建事务
CREATE PROCEDURE updateSno(
    IN oldSno CHAR(9), 
    IN newSno CHAR(9))
BEGIN
    ALTER TABLE Score
    DROP CONSTRAINT fk_Score_Sno;
    UPDATE Score
    SET Sno = newSno
    WHERE Sno = oldSno;
    
    ALTER TABLE ppdate
    DROP CONSTRAINT fk_PPDate_Sno;
    UPDATE ppdate
    SET Sno = newSno
    WHERE Sno = oldSno;

    ALTER TABLE Stupassword
    DROP CONSTRAINT fk_Stupassword_Sno;
    UPDATE Stupassword
    SET Sno = newSno
    WHERE Sno = oldSno;

    UPDATE Student
    SET Sno = newSno
    WHERE Sno = oldSno;
    
    
    ALTER TABLE Score
    ADD CONSTRAINT fk_Score_Sno FOREIGN KEY (Sno) REFERENCES Student(Sno);
    ALTER TABLE ppdate
    ADD CONSTRAINT fk_PPDate_Sno FOREIGN KEY (Sno) REFERENCES Student(Sno);
    ALTER TABLE Stupassword
    ADD CONSTRAINT fk_Stupassword_Sno FOREIGN KEY (Sno) REFERENCES Student(Sno);

END


#存储过程：更新课号
CREATE PROCEDURE updateCid(
    IN old_Cid CHAR(4),
    IN new_Cid CHAR(4))
BEGIN
    ALTER TABLE Score
    DROP CONSTRAINT fk_Score_Cid;
    UPDATE Score
    SET Cid = new_Cid
    WHERE Cid = old_Cid;
    UPDATE Course
    SET Cid = new_Cid
    WHERE Cid = old_Cid;
    ALTER TABLE Score
    ADD CONSTRAINT fk_Score_Cid FOREIGN KEY (Cid) REFERENCES Course(Cid);
END

DROP FUNCTION IF EXISTS calCredit;
#函数：计算学生的总学分
CREATE FUNCTION calCredit(Sno CHAR(9)) RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE totalCredit INT;
    SELECT SUM(Course.Credit) INTO totalCredit
    FROM Course
    WHERE Course.Cid IN (
        SELECT Score.Cid
        FROM Score
        WHERE Score.Sno = Sno
    );
    RETURN totalCredit;
END

DROP TRIGGER IF EXISTS deleteStudent;
DROP TRIGGER IF EXISTS deleteCourse;
DROP TRIGGER IF EXISTS deletePP;
DROP TRIGGER IF EXISTS addStudent;



#触发器：删除学生时删除学生的成绩和奖惩信息
CREATE TRIGGER deleteStudent
BEFORE DELETE ON Student
FOR EACH ROW
BEGIN
    DELETE FROM Score WHERE Score.Sno = OLD.Sno;
    DELETE FROM PPDate WHERE PPDate.Sno = OLD.Sno;
    DELETE FROM Stupassword WHERE Stupassword.Sno = OLD.Sno;
END

#触发器：删除课程时删除课程的成绩
CREATE TRIGGER deleteCourse
BEFORE DELETE ON Course
FOR EACH ROW
BEGIN
    DELETE FROM Score WHERE Score.Cid = OLD.Cid;
END

#触发器：删除奖惩信息时删除奖惩日期
CREATE TRIGGER deletePP
BEFORE DELETE ON PrizePunish
FOR EACH ROW
BEGIN
    DELETE FROM PPDate WHERE PPDate.PPid = OLD.PPid;
END

#触发器：添加学生时自动注册账号，密码为123456
CREATE TRIGGER addStudent
AFTER INSERT ON Student
FOR EACH ROW
BEGIN
    INSERT INTO Stupassword(Sno, password) VALUES (NEW.Sno, '123456');
END
