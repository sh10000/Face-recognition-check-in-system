from django.shortcuts import render
from django.http import HttpResponse
from app1 import models
from django.core.files.base import ContentFile


# Create your views here.

# 主页，处理教师和管理员登录，学生签到
def index(request):
    return render(request, "ManageIndex.html")


def user_list(request):
    return render(request, "user.html")


def user_list(request):
    return render(request, "user.html")


def tpl(request):
    return render(request, "tpl.html")


def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    return render(request, "register.html")


def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username, password)
    return render(request, "ManagementLogin.html")


def login_post(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # username = request.POST['username']
        # password = request.POST['password']
        print(username, password)
    return render(request, "ManageIndex.html")


def pic_upload(request):
    return render(request, "PicUploadTest.html")


def updateinfo(request):
    if request.method == 'POST':
        new_img = models.mypicture(
            photo=request.FILES.get('photo'),
            user=request.FILES.get('photo').name
        )
        new_img.save()
        return HttpResponse('上传成功！')
    return render(request, 'PicUploadTest.html')

#教师功能组
def teacher(request):
    return render(request, "app1/templates/teacher/teacher.html")
def publishSign(request):
    return render(request, "app1/templates/teacher/SignPublish.html")

def signResult(request):
    return render(request, "app1/templates/teacher/SignResult.html")



#管理员功能组
def manageIndex(request):
    return render(request, "ManageIndex.html")
def manageCourse(request):
    return render(request, "ManageCourse.html")

def manageTeacher(request):
    return render(request, "ManageTeacher.html")

def manageStudent(request):
    return render(request, "ManageTeacher.html")

#学生签到页面

