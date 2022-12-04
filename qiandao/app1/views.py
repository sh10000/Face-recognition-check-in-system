from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# 主页，处理教师和管理员登录，学生签到
def index(request):
    return  HttpResponse("欢迎使用")

#教师功能组
def teacher(request):
    return render(request, "app1/templates/teacher/teacher.html")
def publishSign(request):
    return render(request, "qiandao/app1/templates/teacher/SignPublish.html")

def signResult(request):
    return  render(request, "app1/templates/teacher/SignResult.html")



#管理员功能组
