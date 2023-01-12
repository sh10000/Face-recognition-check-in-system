from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from app1 import models
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login
from functools import wraps
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from django.apps import apps
import app1


# Create your views here.

# 检查登录状态
def check_login(func):
    @wraps(func)  # 装饰器修复技术
    def inner(request, *args, **kwargs):
        # 已经登录过的继续执行
        ret = request.get_signed_cookie("is_login", default="0", salt="dsb")
        if ret == "1":
            return func(request, *args, **kwargs)
        # 没有登录过的跳转登录界面
        else:
            return redirect("/login")
            # #获取当前访问的URl
            # next_url = request.path_info
            # print(next_url)
            # return redirect("/login/?next={}".format(next_url))

    return inner


def check_duplicate(model_name, field_name):
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            form = request.POST
            model = apps.get_model('app1', model_name)
            print(model)
            if model.objects.filter(**{field_name: form.get(field_name)}).exists():
                kwargs['err_message'] = f'{field_name} already exists.'
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return _decorator


# 主页，处理教师和管理员登录，学生签到
@check_login
def index(request):
    return redirect("/login")


@check_login
def user_list(request):
    return render(request, "user.html")


@check_login
def user_list(request):
    return render(request, "user.html")


@check_login
def tpl(request):
    return render(request, "tpl.html")


def login(request):
    errmsg = ""
    if request.method == "POST":
        usertype = request.POST['seltype']
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.GET.get("next")
        # 学生登录
        if usertype == "学生":
            stu_obj = models.Student.objects.filter(studentNo=username, password=password)
            if stu_obj:
                if next_url:
                    rep = redirect(next_url)
                else:
                    rep = redirect('/student')
                rep.set_signed_cookie("is_login", "1", salt="dsb", max_age=60 * 60 * 24 * 7)
                rep.set_signed_cookie("username", username, salt="dsb", max_age=60 * 60 * 24 * 7)
                return rep
            else:
                errmsg = "用户名或密码输入错误"
        # 管理员登录
        elif usertype == "管理员":
            object = models.Admin.objects.filter(adminNo=username, password=password)
            if object:
                if next_url:
                    rep = redirect(next_url)
                else:
                    rep = redirect('/manage')
                rep.set_signed_cookie("is_login", "1", salt="dsb", max_age=60 * 60 * 24 * 7)
                rep.set_signed_cookie("username", username, salt="dsb", max_age=60 * 60 * 24 * 7)
                return rep
            else:
                errmsg = "用户名或密码输入错误"
        # 教师登录
        else:
            object = models.Teacher.objects.filter(teacherNo=username, password=password)
            if object:
                if next_url:
                    rep = redirect(next_url)
                else:
                    rep = redirect('/teacher')
                rep.set_signed_cookie("is_login", "1", salt="dsb", max_age=60 * 60 * 24 * 7)
                rep.set_signed_cookie("username", username, salt="dsb", max_age=60 * 60 * 24 * 7)
                return rep
            else:
                errmsg = "用户名或密码输入错误"
    else:
        errmsg = "您还未登录！"
    return render(request, 'login.html', {"errmsg": errmsg})


@check_login
def logout(request):
    rep = redirect("/login/")
    rep.delete_cookie("is_login")
    rep.delete_cookie("username")
    return rep


@check_duplicate('Student', 'studentNo')
def register(request, err_message=None):
    if request.method == 'GET':
        return render(request, "register.html")
    if err_message:
        return render(request, "register.html", {"err_message": err_message})
    user = request.POST.get("name")
    pwd = request.POST.get("password")
    studentNo = request.POST.get("studentNo")
    img = request.FILES.get('img')
    if studentNo == "":
        return render(request, "register.html", {'err_message': "学号不得为空！"})
    elif user == "":
        return render(request, "register.html", {'err_message': "姓名不得为空！"})
    elif pwd == "":
        return render(request, "register.html", {'err_message': "密码不得为空！"})
    elif img is None:
        return render(request, "register.html", {'err_message': "请上传照片！"})
    else:
        rep = redirect('/student')
        rep.set_signed_cookie("is_login", "1", salt="dsb", max_age=60 * 60 * 24 * 7)
        rep.set_signed_cookie("username", studentNo, salt="dsb", max_age=60 * 60 * 24 * 7)
        return rep


@check_login
def pic_upload(request):
    return render(request, "PicUploadTest.html")


@check_login
def updateinfo(request):
    if request.method == 'POST':
        new_img = models.mypicture(
            photo=request.FILES.get('photo'),
            user=request.FILES.get('photo').name
        )
        new_img.save()
        return HttpResponse('上传成功！')
    return render(request, 'PicUploadTest.html')


# 教师功能组
@check_login
def teacher(request):
    teaName = request.get_signed_cookie("username", salt="dsb")
    cursor = connection.cursor()
    sql = "SELECT classNo, courseNo, courseName, grade " \
          "FROM renLianShiBie1.app1_class a, renLianShiBie1.app1_course b " \
          "WHERE a.course_id = b.courseNo AND a.teacher_id = " + teaName + ";"
    cursor.execute(sql)
    res = cursor.fetchall()
    return render(request, "Teacher/Tmain.html", {"teaName": teaName, "res": res})


@check_login
def classInfo(request):
    data_list = models.Class.objects.all()
    print(data_list)
    return render(request, "Classinfo.html", {"n1": data_list})


@check_login
def signpublish(request):
    teaName = request.get_signed_cookie("username", salt="dsb")
    courseNo = request.GET.get("courseNo")
    classNo = request.GET.get("classNo")
    print(courseNo, classNo)
    if classNo is None or courseNo is None:
        return redirect("/teacher")
    course = models.Course.objects.get(courseNo=courseNo)
    courseName = course.courseName
    if request.method == "GET":
        return render(request, "Teacher/SignPublish.html",
                      {"teaName": teaName, "courseName": courseName, "datetime": datetime.datetime.now(),
                       "courseNo": courseNo, "classNo": classNo})
    # 发布签到
    qianDaoName = request.POST.get("qianDaoName")
    pubtime = datetime.datetime.now()
    dueTime = request.POST.get("dueTime")
    courseNo = request.POST.get("courseNo")
    classNo = request.POST.get("classNo")
    if dueTime == "5min":
        timedelta = datetime.timedelta(minutes=5)
    elif dueTime == "10min":
        timedelta = datetime.timedelta(minutes=10)
    elif dueTime == "15min":
        timedelta = datetime.timedelta(minutes=15)
    elif dueTime == "30min":
        timedelta = datetime.timedelta(minutes=30)
    elif dueTime == "1h":
        timedelta = datetime.timedelta(minutes=60)
    dueTime = pubtime + timedelta
    print("123", qianDaoName, pubtime, dueTime, courseNo, classNo)
    new_qiandao = models.QianDao(
        qianDaoName=qianDaoName,
        courseName=courseName,
        class1_id=classNo,
        pubtime=pubtime,
        duetime=dueTime,
        teacherNo_id=teaName
    )
    new_qiandao.save()
    qid = new_qiandao.id
    # 将学生加入到学生签到表
    cursor = connection.cursor()
    sql = "SELECT student_id FROM renLianShiBie1.app1_class_students WHERE class_id =" + classNo + ";"
    cursor.execute(sql)
    sid_list = cursor.fetchall()
    for row in sid_list:
        sid = row[0]
        #  cursor2 = connection.cursor()
        #  sql2 = "INSERT INTO INSERT INTO renLianShiBie1.app1_stuqiandao VALUES (null,%s,%s,null,False)" % (str(qid), str(sid))
        #  cursor2.execute(sql2)
        new_sqiandao = models.StuQianDao(
            QianDaoId_id=qid,
            studentNo_id=sid,
            status='未签到'
        )
        new_sqiandao.save()
    return redirect("/signresult/?Qid=" + str(new_qiandao.id))


@check_login
def signresult(request):
    Qid = request.GET.get("Qid")
    print(Qid)
    if Qid is None:
        return redirect("/teasigninfo/")
    else:
        cursor = connection.cursor()
        sql = "SELECT studentNo, `name`, QTime, status from renLianShiBie1.app1_student a, renLianShiBie1.app1_stuqiandao b " \
              "where a.studentNo = b.studentNo_id and b.status='已签到' and b.QianDaoId_id= " + Qid + ";"
        cursor.execute(sql)
        res = cursor.fetchall()
    teaName = request.get_signed_cookie("username", salt="dsb")
    return render(request, "Teacher/SignResult.html", {"teaName": teaName, "res": res, "Qid": Qid})


@check_login
def unsignresult(request):
    Qid = request.GET.get("Qid")
    print("qid:", Qid)
    if Qid is None:
        return redirect("/teasigninfo/")
    else:
        cursor = connection.cursor()
        sql = "SELECT studentNo, `name`, QTime, status from renLianShiBie1.app1_student a, renLianShiBie1.app1_stuqiandao b " \
              "where a.studentNo = b.studentNo_id and b.status='未签到' and b.QianDaoId_id= " + Qid + ";"
        cursor.execute(sql)
        res = cursor.fetchall()
    teaName = request.get_signed_cookie("username", salt="dsb")
    return render(request, "Teacher/UnSignResult.html", {"teaName": teaName, "res": res, "Qid": Qid})


@check_login
def teasigninfo(request):
    teaName = request.get_signed_cookie("username", salt="dsb")
    cursor = connection.cursor()
    sql = "SELECT id, qianDaoName, courseName, class1_id, pubtime from renLianShiBie1.app1_qiandao a where " \
          "teacherNo_id=" + teaName + " order by pubtime desc;"
    cursor.execute(sql)
    res = cursor.fetchall()
    return render(request, "Teacher/Signrecord.html", {"teaName": teaName, "res": res})


@check_login
def setunsign(request):
    qid = request.GET.get("qid")
    sid = request.GET.get("sid")
    models.StuQianDao.objects.filter(studentNo_id=sid).update(status="未签到")
    return redirect("/signresult/?Qid=" + qid)


@check_login
def setsign(request):
    qid = request.GET.get("qid")
    sid = request.GET.get("sid")
    models.StuQianDao.objects.filter(studentNo_id=sid).update(status="已签到")
    return redirect("/unsignresult/?Qid=" + qid)


@check_login
def stopsign(request):
    qid = request.GET.get("Qid")
    print(qid)
    print(models.QianDao.objects.filter(id=qid))
    models.QianDao.objects.filter(id=qid).update(duetime=datetime.datetime.now())
    print(models.QianDao.objects.filter(id=qid))
    return redirect("/signresult/?Qid=" + qid)


@check_login
def tcourse(request):
    teaName = request.get_signed_cookie("username", salt="dsb")
    return render(request, "Teacher/Tcourse.html", {"teaName": teaName})


# 管理员功能组
@check_login
def manageIndex(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    return render(request, "Manage/main.html", {"admName": admName})


@check_login
def manageStudent(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    ask = request.GET.get("ask")
    if (ask != None):
        studentNo = models.Student.objects.filter(name__contains=ask)
        return render(request, "Manage/ManageStudent.html", {"admName": admName, "n1": studentNo})
    if (ask == None):
        student_list = models.Student.objects.all()
        return render(request, "Manage/ManageStudent.html", {"admName": admName, "n1": student_list})


# 管理员增加学生信息
@check_login
def addstudent(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method == 'GET':
        return render(request, "Manage/add-student.html", {"admName": admName})
    user = request.POST.get("name")
    pwd = request.POST.get("password")
    studentNo = request.POST.get("studentNo")
    img = request.FILES.get('img')
    if img != None:
        img_name = img.name
        models.Student.objects.create(studentNo=studentNo, name=user, password=pwd, photo=img, img_name=img_name)
        return redirect("/managestudent")
    else:
        return redirect("/addstudent?Qid=" + str(1))


@check_login
def manageStudentDelete(request):
    nid = request.GET.get('nid')
    models.Student.objects.filter(studentNo=nid).delete()
    return redirect("/managestudent")


# 管理员修改学生信息
@check_login
def manageStudentModify(request, nid):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method == 'GET':
        studentNo = models.Student.objects.filter(studentNo=nid).first()
        return render(request, "Manage/modify-student.html", {"n1": studentNo, "nid": nid})
    user = request.POST.get("name")
    pwd = request.POST.get("password")
    studentNo = request.POST.get("studentNo")
    img = request.FILES.get('img')
    print('打印图片', img)
    if (img != None):
        img_name = img.name
        models.StudentPhoto.objects.create(photo=img)
        models.Student.objects.filter(studentNo=nid).update(studentNo=nid, name=user, password=pwd, photo=img,
                                                            img_name=img_name)
        return redirect("/managestudent?Qid=" + str(1))
    else:
        models.Student.objects.filter(studentNo=nid).update(studentNo=nid, name=user, password=pwd)
        return redirect("/addstudent?Qid=" + str(1))


# 管理员课程
@check_login
def manageCourse(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    ask = request.GET.get("ask")
    if (ask != None):
        courseNo = models.Course.objects.filter(courseName__contains=ask)
        return render(request, "Manage/ManageCourse.html", {"admName": admName, "n1": courseNo})
    if (ask == None):
        course_list = models.Course.objects.all()
        return render(request, "Manage/ManageCourse.html", {"admName": admName, "n1": course_list})


@check_login
def addcourse(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method == 'GET':
        return render(request, "Manage/add-course.html")
    print(request.POST)
    courseNo = request.POST.get("courseNo")
    courseName = request.POST.get("courseName")
    grade = request.POST.get("grade")
    models.Course.objects.create(courseNo=courseNo, courseName=courseName, grade=grade)
    return redirect("/managecourse")


# 管理员删除学生信息
@check_login
def manageCourseDelete(request):
    nid = request.GET.get('nid')
    models.Course.objects.filter(courseNo=nid).delete()
    return redirect("/managecourse")


@check_login
def manageCourseModify(request, nid):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method == 'GET':
        studentNo = models.Course.objects.filter(courseNo=nid).first()
        return render(request, "Manage/modify-course.html", {"n1": studentNo, "nid": nid})
    nid = request.POST.get("nid")
    name = request.POST.get("courseName")
    pwd = request.POST.get("password")
    models.Course.objects.filter(courseNo=nid).update(courseNo=nid, courseName=name, grade=pwd)
    return redirect("/managecourse")


# 管理员教师
@check_login
def manageTeacher(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    ask = request.GET.get("ask")
    if (ask != None):
        teacherNo = models.Teacher.objects.filter(name__contains=ask)
        return render(request, "Manage/ManageTeacher.html", {"admName": admName, "n1": teacherNo})
    if (ask == None):
        teacher_list = models.Teacher.objects.all()
        return render(request, "Manage/ManageTeacher.html", {"admName": admName, "n1": teacher_list})


@check_login
def addteacher(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method == 'GET':
        return render(request, "Manage/add-teacher.html")
    print(request.POST)
    teacherNo = request.POST.get("teacherNo")
    name = request.POST.get("name")
    user = request.POST.get("user")
    password = request.POST.get("password")
    models.Teacher.objects.create(teacherNo=teacherNo, name=name, user=user, password=password)
    return redirect("/manageteacher")


@check_login
def manageTeacherDelete(request):
    nid = request.GET.get('nid')
    models.Teacher.objects.filter(teacherNo=nid).delete()
    return redirect("/manageteacher")


@check_login
def manageTeacherModify(request, nid):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method == 'GET':
        studentNo = models.Teacher.objects.filter(teacherNo=nid).first()
        return render(request, "Manage/modify-teacher.html", {"n1": studentNo, "nid": nid})
    nid = request.POST.get("nid")
    name = request.POST.get("name")
    user = request.POST.get("user")
    password = request.POST.get("password")
    models.Teacher.objects.filter(teacherNo=nid).update(teacherNo=nid, name=name, password=password, user=user)
    return redirect("/manageteacher")


# 管理员教师
# 学生课程界面
@check_login
def student(request):
    stuName = request.get_signed_cookie("username", salt="dsb")
    ask = request.GET.get("ask")
    if (ask == None):
        cursor = connection.cursor()
        sql = "SELECT course_id,courseName,classNo,`name` from  renLianShiBie1.app1_class a, renLianShiBie1.app1_course b ,renLianShiBie1.app1_class_students c,renLianShiBie1.app1_teacher d WHERE a.teacher_id=d.teacherNo and a.course_id=b.courseNo and a.classNo=c.class_id and c.student_id=" + stuName
        cursor.execute(sql)
        res = cursor.fetchall()
        return render(request, "Student/Smain.html", {"stuName": stuName, "n1": res})
    else:
        cursor = connection.cursor()
        sql = "SELECT course_id,courseName,classNo,`name` from  renLianShiBie1.app1_class a, renLianShiBie1.app1_course b ,renLianShiBie1.app1_class_students c,renLianShiBie1.app1_teacher d WHERE a.teacher_id=d.teacherNo and a.course_id=b.courseNo and a.classNo=c.class_id and c.student_id=" + stuName + " and courseName like '%" + ask + "%'"
        cursor.execute(sql)
        res = cursor.fetchall()
        return render(request, "Student/Smain.html", {"stuName": stuName, "n1": res})


# 学生添加课程界面
@check_login
def addCourselist(request):
    stuName = request.get_signed_cookie("username", salt="dsb")
    cursor = connection.cursor()
    ask = request.GET.get("ask")
    if (ask == None):
        sql = "SELECT  course_id, courseName,classNo,`name` From   renLianShiBie1.app1_class a, renLianShiBie1.app1_course b ,renLianShiBie1.app1_teacher d where    a.teacher_id=d.teacherNo and a.course_id=b.courseNo  and classNo not in ( SELECT classNo from  renLianShiBie1.app1_class a, renLianShiBie1.app1_course b ,renLianShiBie1.app1_class_students c,renLianShiBie1.app1_teacher d WHERE a.teacher_id=d.teacherNo and a.course_id=b.courseNo and a.classNo=c.class_id and student_id=" + stuName + ")"
        cursor.execute(sql)
        res = cursor.fetchall()
        return render(request, "Student/add-course.html", {"stuName": stuName, "n1": res})
    else:
        sql = "SELECT  course_id, courseName,classNo,`name` From   renLianShiBie1.app1_class a, renLianShiBie1.app1_course b ,renLianShiBie1.app1_teacher d where    a.teacher_id=d.teacherNo and a.course_id=b.courseNo  and courseName like '%" + ask + "%' and classNo not in ( SELECT classNo from  renLianShiBie1.app1_class a, renLianShiBie1.app1_course b ,renLianShiBie1.app1_class_students c,renLianShiBie1.app1_teacher d WHERE a.teacher_id=d.teacherNo and a.course_id=b.courseNo and a.classNo=c.class_id and student_id=" + stuName + ")"
        cursor.execute(sql)
        res = cursor.fetchall()
        return render(request, "Student/add-course.html", {"stuName": stuName, "n1": res})


# 学生增加课程
@check_login
def addCourse(request):
    classid = request.GET.get('classid')
    name = request.GET.get('name')
    cursor = connection.cursor()
    sql = "insert into renLianShiBie1.app1_class_students(class_id,student_id) values (" + classid + "," + name + ")"
    cursor.execute(sql)
    res = cursor.fetchall()
    return redirect("/addstudentcourselist")


# 签到界面
@check_login
def sign(request):
    stuName = request.get_signed_cookie("username", salt="dsb")
    classNo = request.GET.get('classNo')
    cursor = connection.cursor()
    sql = "SELECT  a.id,now()  FROM  renLianShiBie1.app1_qiandao a,renLianShiBie1.app1_class_students b WHERE pubtime <= now() AND duetime >= now() and class1_id=" + classNo + " and a.class1_id=b.class_id and student_id =" + stuName
    cursor.execute(sql)
    res = cursor.fetchall()
    if len(res) == 0:
        return redirect("/student?Qid=" + str(1))
    else:
        return render(request, "Student/Sign.html", {"stuName": stuName, 'classNo': classNo})


@check_login
@csrf_exempt
def signed(request):
    stuName = request.get_signed_cookie("username", salt="dsb")
    photo = request.POST.get("photo")
    print(photo)
    classNo = request.GET.get('classNo')
    return HttpResponse("success!!")


@check_login
def signinfo(request):
    stuName = request.get_signed_cookie("username", salt="dsb")
    classNo = request.GET.get('classNo')
    cursor = connection.cursor()
    sql = "select classNo,b.courseName,QTime,status from renLianShiBie1.app1_class a,renLianShiBie1.app1_course b,renLianShiBie1.app1_stuqiandao c,renLianShiBie1.app1_qiandao d where a.course_id=b.courseNo and c.QianDaoId_id=d.id and d.class1_id =a.classNo and studentNo_id=" + stuName + " and classNo=" + classNo + " order by c.id DESC"
    cursor.execute(sql)
    res = cursor.fetchall()
    return render(request, "Student/SignInfo.html", {"stuName": stuName, "res": res})


# 前端测试类
@csrf_exempt
def ajaxtest(request):
    photo = request.POST.get("photo")
    print(photo)
    res = json.dumps(photo)
    # classNo=request.GET.get('classNo')
    return HttpResponse(res)
