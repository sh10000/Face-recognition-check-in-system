from django.shortcuts import render,redirect
from django.http import HttpResponse
from app1 import models
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login
from functools import wraps


# Create your views here.

# 检查登录状态
def check_login(func):
    @wraps(func)  #装饰器修复技术
    def inner(request,*args,**kwargs):
        #已经登录过的继续执行
        ret = request.get_signed_cookie("is_login", default="0", salt="dsb")
        if ret == "1":
            print(123)
            return func(request,*args,**kwargs)
        #没有登录过的跳转登录界面
        else:
            print(456)
            return redirect("/login")
            # #获取当前访问的URl
            # next_url = request.path_info
            # print(next_url)
            # return redirect("/login/?next={}".format(next_url))
    return inner

# 主页，处理教师和管理员登录，学生签到
@check_login
def index(request):
    stuName = request.get_signed_cookie("username", salt="dsb")
    return render(request, "test-studentdis.html", {"stuName": stuName})


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
                    rep = redirect('/index/')
                rep.set_signed_cookie("is_login", "1", salt="dsb", max_age=60 * 60 * 24 * 7)
                rep.set_signed_cookie("username", username, salt="dsb", max_age=60 * 60 * 24 * 7)
                return rep
            else:
                errmsg="用户名或密码输入错误"
        # 管理员登录
        elif usertype == "管理员":
            object = models.Admin.objects.filter(adminNo=username, password=password)
            if object:
                if next_url:
                    rep = redirect(next_url)
                else:
                    rep = redirect('/manager')
                rep.set_signed_cookie("is_login", "1", salt="dsb", max_age=60 * 60 * 24 * 7)
                rep.set_signed_cookie("username", username, salt="dsb", max_age=60 * 60 * 24 * 7)
                return rep
            else:
                errmsg="用户名或密码输入错误"
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
    return render(request, 'login.html',{"errmsg":errmsg})

@check_login
def logout(request):
    rep = redirect("/login/")
    rep.delete_cookie("is_login")
    rep.delete_cookie("username")
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
    return render(request, "TeacherCourse.html", {"teaName":teaName})

@check_login
def classInfo(request):
    data_list = models.Class.objects.all()
    print(data_list)
    return render(request, "Classinfo.html", {"n1": data_list})

@check_login
def publishSign(request):
    return render(request, "app1/templates/teacher/SignPublish.html")


@check_login
def signResult(request):
    return render(request, "app1/templates/teacher/SignResult.html")


# 管理员功能组
@check_login
def manageIndex(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    student_list = models.Student.objects.all()
    for i in student_list:
      print(i.studentNo,i.name,i.password,i.photo)
    return render(request, "ManageIndex.html", {"admName": admName,"n1": student_list})

#管理员删除学生信息
@check_login
def managerStudentDelete(request):
      nid=request.GET.get('nid')
      models.Student.objects.filter(studentNo=nid).delete()
      return redirect("/manager/")

#管理员增加学生信息
def  managerStudentAdd(request):
      if request.method=='GET':
            return render(request,"info_add.html")
      print(request.POST)
      user=request.POST.get("user")
      pwd=request.POST.get("pwd")
      studentNo=request.POST.get("studentNo")
      models.Student.objects.create(studentNo=studentNo,name=user,password=pwd)
      return redirect("/manager/")
def managerStudentModify(request):
      if request.method=='GET':
            return render(request,"info_add.html")
      user=request.POST.get("user")
      pwd=request.POST.get("pwd")
      studentNo=request.POST.get("studentNo")
      models.Student.objects.filter(studentNo=studentNo).update(name=user,password=pwd)
      return redirect("/manager/")

@check_login
def manageCourse(request):
    return render(request, "ManageCourse.html")


@check_login
def manageTeacher(request):
    return render(request, "ManageTeacher.html")


@check_login
def manageStudent(request):
    return render(request, "ManageTeacher.html")

# 学生签到页面
@check_login
def studentQianDao(request):
    return render(request,"StudentSign.html")
