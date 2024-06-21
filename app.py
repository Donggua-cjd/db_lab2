
from flask import Flask, request, render_template, redirect, url_for
import pymysql



app = Flask(__name__)

dbhost = '127.0.0.1'
dbuser = 'root'
dbpass = '142857'
dbname = 'lab'

db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
cursor = db.cursor()

#与学生有关的操作
def get_student():
    cursor.execute('SELECT * FROM student')
    return cursor.fetchall()

def get_student_by_id(id):
    cursor.execute('SELECT * FROM student WHERE Sno = %s' % id)
    return cursor.fetchone()

def get_student_by_name(name):
    sql = "SELECT * FROM student WHERE Sname LIKE %s"
    cursor.execute(sql,(name,))
    return cursor.fetchall()

def add_student(id, name, sex, dept, img):
    sql = ('INSERT INTO student(Sno,Sname,Ssex,Sdept,Spic) VALUES(%s, %s, %s, %s, %s)')
    try:
        cursor.execute(sql,(id, name, sex, dept, img))
        db.commit()
    except Exception as e:
        print(f"Error:{e}")
        db.rollback()
        return
    
def update_student(oldid,newid,name,sex,dept,img):
    sql = ("UPDATE student SET Sname='%s',Ssex='%s',Sdept='%s',Spic='%s' WHERE Sno='%s'" % (name, sex, dept, img, oldid))
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"Error:{e}")
        db.rollback()
        return
    #更新学号
    if oldid != newid:
        sql = ("CALL updateSno(%s, %s)")
        try:
            cursor.execute(sql,(oldid,newid))
            db.commit()
        except Exception as e:
            print(f"Error:{e}")
            db.rollback()
            return
        
def delete_student(id):
    sql = 'DELETE FROM Student WHERE Sno=%s'
    try:
        cursor.execute(sql,(id,))
        db.commit()
    except Exception as e:
        print(f"Error:{e}")
        db.rollback()
        return 

@app.route('/')
def index():
    return redirect(url_for('loginadmin'))

@app.route('/loginadmin',methods=['GET','POST'])
def loginadmin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 检查用户名和密码是否正确
        cursor.execute('SELECT * FROM admin WHERE name = %s AND password = %s', (username, password))
        admin = cursor.fetchone()
        if admin:
            # 登录成功，跳转到 menu route
            return redirect(url_for('indexadmin'))
        else:
            # 登录失败，提示用户名或密码错误
            return 'Admin login failed: Incorrect username or password'
    else:
        # GET 请求，显示登录表单
        return render_template('loginadmin.html')
    
@app.route('/loginstu', methods=['GET','POST'])
def loginstu():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 检查用户名和密码是否正确
        cursor.execute('SELECT * FROM stupassword WHERE Sno = %s AND password = %s', (username, password))
        admin = cursor.fetchone()
        if admin:
            # 登录成功，跳转到 indexstu，并且传id过去
            return redirect(url_for('indexstu',id=username))
        else:
            # 登录失败，提示用户名或密码错误
            return 'Admin login failed: Incorrect username or password'
    else:
        # GET 请求，显示登录表单
        return render_template('loginstu.html')

@app.route('/indexadmin')
def indexadmin():
    return render_template('indexadmin.html')


@app.route('/student')
def student_info():
    return render_template('student.html', students=get_student())

@app.route('/modifystu/<id>', methods=['GET', 'POST'])
def modifystu(id):
    if request.method == 'GET':
        return render_template('modifystu.html', student=get_student_by_id(id))
    else:
        oldid = request.form.get('studentId')
        newid = request.form.get('newStudentId')
        name = request.form.get('studentName')
        sex = request.form.get('studentGender')
        dept = request.form.get('studentMajor')
        img = request.form.get('studentImage')
        update_student(oldid, newid, name, sex, dept, img)
        return redirect(url_for('student_info'))
    
@app.route('/addstu', methods=['GET', 'POST'])
def addstu():
    if request.method == 'GET':
        return render_template('addstu.html')
    else:
        id = request.form.get('studentId')
        name = request.form.get('studentName')
        sex = request.form.get('studentGender')
        dept = request.form.get('studentMajor')
        img = request.form.get('studentImage')
        add_student(id, name, sex, dept, img)
        return redirect(url_for('student_info'))
    
@app.route('/deletestu/<id>')
def deletestu(id):
    delete_student(id)
    return redirect(url_for('student_info'))

@app.route('/searchstu', methods=['POST'])
def searchstu():
   name = request.form.get('studentName')
   if name != '':
        students = get_student_by_name(name)
        return render_template('student.html', students=students)
   else:
    #    js_code = "<script>alert('请输入姓名！');history.back();</script>"
    #    return js_code
        return redirect(url_for('student_info'))
   
@app.route('/changepw/<id>', methods=['GET', 'POST'])
def changepw(id):
    if request.method == 'GET':
        return render_template('changepw.html', student=get_student_by_id(id))
    else:
        id = request.form.get('studentId')
        oldpw = request.form.get('oldPassword')
        newpw = request.form.get('newPassword')
        cursor.execute('SELECT * FROM stupassword WHERE Sno = %s AND password = %s', (id, oldpw))
        admin = cursor.fetchone()
        if admin:
            cursor.execute('UPDATE stupassword SET password = %s WHERE Sno = %s', (newpw, id))
            db.commit()
            return redirect(url_for('indexstu',id=id))
        else:
            return 'Change password failed: Incorrect old password'

def get_courses():
    cursor.execute('SELECT * FROM course')
    return cursor.fetchall()

def get_course_by_id(cid):
    cursor.execute('SELECT * FROM course WHERE Cid = "%s"' % cid)
    return cursor.fetchone()

def get_course_by_name(name):
    sql = "SELECT * FROM course WHERE Cname LIKE %s"
    cursor.execute(sql,(name,))
    return cursor.fetchall()

def add_course(id, name, credit):
    sql = ('INSERT INTO course(Cid,Cname,Credit) VALUES(%s, %s, %s)')
    try:
        cursor.execute(sql,(id, name, credit))
        db.commit()
    except Exception as e:
        print(f"Error:{e}")
        db.rollback()
        return
    
def update_course(oldid,newid,name,credit):
    sql = ("UPDATE course SET Cname='%s',Credit='%s' WHERE Cid='%s'" % (name, credit, oldid))
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"Error:{e}")
        db.rollback()
        return
    #更新课程号
    if oldid != newid:
        sql = ("CALL updateCid(%s, %s)")
        try:
            cursor.execute(sql,(oldid,newid))
            db.commit()
        except Exception as e:
            print(f"Error:{e}")
            db.rollback()
            return
        
def delete_course(id):
    sql = 'DELETE FROM course WHERE Cid=%s'
    try:
        cursor.execute(sql,(id,))
        db.commit()
    except Exception as e:
        print(f"Error:{e}")
        db.rollback()
        return



@app.route('/course')
def course_info():
    return render_template('course.html', courses=get_courses())

@app.route('/addcourse', methods=['GET', 'POST'])
def addcourse():
    if request.method == 'GET':
        return render_template('addcourse.html')
    else:
        id = request.form.get('courseId')
        name = request.form.get('courseName')
        credit = request.form.get('courseCredit')
        add_course(id, name, credit)
        return redirect(url_for('course_info'))
    
@app.route('/deletecourse/<id>')
def deletecourse(id):
    delete_course(id)
    return redirect(url_for('course_info'))

@app.route('/modifycourse/<id>', methods=['GET', 'POST'])
def modifycourse(id):
    if request.method == 'GET':
        return render_template('modifycourse.html', course=get_course_by_id(id))
    else:
        oldid = request.form.get('courseId')
        newid = request.form.get('newCourseId')
        name = request.form.get('courseName')
        credit = request.form.get('courseCredit')
        update_course(oldid, newid, name, credit)
        return redirect(url_for('course_info'))

@app.route('/searchcourse', methods=['POST'])
def searchcourse():
    name = request.form.get('courseName')
    if name != '':
          courses = get_course_by_name(name)
          return render_template('course.html', courses=courses)
    else:
        return redirect(url_for('course_info'))

def get_score():
    cursor.execute('SELECT * FROM score')
    return cursor.fetchall()

def add_score(sid,cid,score):
    sql = ('INSERT INTO score(Sno,Cid,Score) VALUES(%s, %s, %s)')
    try:
        cursor.execute(sql,(sid, cid, score))
        db.commit()
    except Exception as e:
        print(f"Error:{e}")
        db.rollback()
        return
    
def delete_score(sid,cid):
    sql = 'DELETE FROM score WHERE Sno=%s AND Cid=%s'
    try:
        cursor.execute(sql,(sid,cid))
        db.commit()
    except Exception as e:
        print(f"Error:{e}")
        db.rollback()
        return

@app.route('/score')
def score_info():
    return render_template('score.html', scores=get_score())

@app.route('/addscore', methods=['GET', 'POST'])
def addscore():
    if request.method == 'GET':
        return render_template('addscore.html')
    else:
        sid = request.form.get('studentId')
        cid = request.form.get('courseId')
        score = request.form.get('score')
        add_score(sid,cid,score)
        return redirect(url_for('score_info'))

@app.route('/deletescore/<sid>/<cid>')
def deletescore(sid,cid):
    delete_score(sid,cid)
    return redirect(url_for('score_info'))

@app.route('/modifyscore/<sid>/<cid>', methods=['GET', 'POST'])
def modifyscore(sid,cid):
    if request.method == 'GET':
        return render_template('modifyscore.html',sid=sid,cid=cid)
    else:
        score = request.form.get('score')
        delete_score(sid,cid)
        add_score(sid,cid,score)
        return redirect(url_for('score_info'))

def get_pp():
    cursor.execute('SELECT * FROM prizepunish')
    return cursor.fetchall()
    
def add_pp(ppid,ppname):
    sql = ('INSERT INTO prizepunish(PPid,PPcontent) VALUES(%s, %s)')
    try:
        cursor.execute(sql,(ppid, ppname))
        db.commit()
    except Exception as e:
        print(f"Error:{e}")
        db.rollback()
        return
def delete_pp(ppid):
    sql = 'DELETE FROM prizepunish WHERE PPid="%s"' 
    try:
        cursor.execute(sql,(ppid,))
        db.commit()
    except Exception as e:
        print(f"Error:{e}")
        db.rollback()
        return
    
def get_pp_by_id(id):
    cursor.execute('SELECT * FROM prizepunish WHERE PPid = "%s"' % id)
    return cursor.fetchone()
    
def update_pp(id,name):
    sql = ("UPDATE prizepunish SET PPcontent='%s' WHERE PPid='%s'" % (name, id))
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"Error:{e}")
        db.rollback()
        return
    


@app.route('/pp')
def pp_info():
    return render_template('pp.html', pps=get_pp())

@app.route('/addpp', methods=['GET', 'POST'])
def addpp():
    if request.method == 'GET':
        return render_template('addpp.html')
    else:
        ppid = request.form.get('ppId')
        ppname = request.form.get('ppContent')
        add_pp(ppid,ppname)
        return redirect(url_for('pp_info'))
    
@app.route('/deletepp/<ppid>')
def deletepp(ppid):
    delete_pp(ppid)
    return redirect(url_for('pp_info'))

@app.route('/modifypp/<ppid>', methods=['GET', 'POST'])
def modifypp(ppid):
    if request.method == 'GET':
        return render_template('modifypp.html', pp=get_pp_by_id(ppid))
    else:
        ppid = request.form.get('ppId')
        ppname = request.form.get('ppContent')
        update_pp(ppid,ppname)
        return redirect(url_for('pp_info'))
    

def get_ppdate():
    cursor.execute('SELECT * FROM ppdate')
    return cursor.fetchall()

def add_ppdate(ppid,sno,ppdate):
    sql = ('INSERT INTO ppdate(PPid,Sno,Date) VALUES(%s, %s, %s)')
    try:
        cursor.execute(sql,(ppid, sno, ppdate))
        db.commit()
    except Exception as e:
        print(f"Error:{e}")
        db.rollback()
        return
    
def delete_ppdate(ppid,sno):
    sql = 'DELETE FROM ppdate WHERE PPid="%s" AND Sno="%s"' % (ppid,sno)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"Error:{e}")
        db.rollback()
        return

@app.route('/ppdate')
def ppdate_info():
    return render_template('ppdate.html', ppdates=get_ppdate())

@app.route('/addppdate', methods=['GET', 'POST'])
def addppdate():
    if request.method == 'GET':
        return render_template('addppdate.html')
    else:
        ppid = request.form.get('ppId')
        sno = request.form.get('studentId')
        ppdate = request.form.get('ppDate')
        add_ppdate(ppid,sno,ppdate)
        return redirect(url_for('ppdate_info'))

@app.route('/deleteppdate/<sno>/<ppid>')
def deleteppdate(ppid,sno):
    delete_ppdate(ppid,sno)
    return redirect(url_for('ppdate_info'))

@app.route('/modifyppdate/<sno>/<ppid>', methods=['GET', 'POST'])
def modifyppdate(ppid,sno):
    if request.method == 'GET':
        return render_template('modifyppdate.html', ppid=ppid,sno=sno)
    else:
        ppdate = request.form.get('ppDate')
        delete_ppdate(ppid,sno)
        add_ppdate(ppid,sno,ppdate)
        return redirect(url_for('ppdate_info'))

def get_score_by_sno(sno):
    sql = "SELECT Course.Cname, Course.Credit, Score.Score FROM Course, Score WHERE Course.Cid = Score.Cid AND Score.Sno = %s"
    cursor.execute(sql,(sno,))
    return cursor.fetchall()

def get_allcredit(sno):
    sql = "SELECT calCredit('%s') as credit" % sno
    cursor.execute(sql)
    return cursor.fetchone()

def get_ppdate_by_sno(sno):
    sql = "SELECT PrizePunish.PPcontent, PPdate.Date FROM PrizePunish, PPdate WHERE PrizePunish.PPid = PPdate.PPid AND PPdate.Sno = %s"
    cursor.execute(sql,(sno,))
    return cursor.fetchall()


@app.route('/indexstu')
def indexstu():
    id = request.args.get('id')
    return render_template('indexstu.html',student=get_student_by_id(id),scores=get_score_by_sno(id),credit=get_allcredit(id),ppdates=get_ppdate_by_sno(id))

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
