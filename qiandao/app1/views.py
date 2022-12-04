from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# 主页，处理教师和管理员登录，学生签到
def index(request):
    return  HttpResponse("欢迎使用")

#
def