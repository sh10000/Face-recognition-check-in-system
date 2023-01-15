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
from PIL import Image
import requests
import base64
import os
from django.http import JsonResponse

endpoint = 'face.cn-north-4.myhuaweicloud.com'
project_id = 'fdde698702e2473f8f12d7c481bbbe5e'
token = 'MIITkwYJKoZIhvcNAQcCoIIThDCCE4ACAQExDTALBglghkgBZQMEAgEwghGlBgkqhkiG9w0BBwGgghGWBIIRknsidG9rZW4iOnsiZXhwaXJlc19hdCI6IjIwMjMtMDEtMTVUMTA6NDk6NDkuMjQ3MDAwWiIsIm1ldGhvZHMiOlsicGFzc3dvcmQiXSwiY2F0YWxvZyI6W10sInJvbGVzIjpbeyJuYW1lIjoidGVfYWRtaW4iLCJpZCI6IjAifSx7Im5hbWUiOiJ0ZV9hZ2VuY3kiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3Nfc3BvdF9pbnN0YW5jZSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2l2YXNfdmNyX3ZjYSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2FfY24tc291dGgtNGMiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3Nfa2FlMSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX0tvb1NlYXJjaENPQlQiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9kd3NfcG9jIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfY2JyX2ZpbGUiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3Nfa2MxX3VzZXJfZGVmaW5lZCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX21lZXRpbmdfZW5kcG9pbnRfYnV5IiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfbWFwX25scCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2VnX2NuIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfcmVkaXM2LWdlbmVyaWMtaW50bCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Rjc19kY3MyLWVudGVycHJpc2UiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF92Y3AiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9jdnIiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9tdWx0aV9iaW5kIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfYV9hcC1zb3V0aGVhc3QtM2QiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9wcm9qZWN0X2RlbCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2NlciIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Nlc19yZXNvdXJjZWdyb3VwX3RhZyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2V2c19yZXR5cGUiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9rb29tYXAiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9ldnNfZXNzZDIiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3NfaXIzeCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2FfY24tc291dGh3ZXN0LTJiIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfY3NlX25hY29zIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfaHdkZXYiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9zZnN0dXJibyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2h2X3ZlbmRvciIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2FfY24tbm9ydGgtNGUiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9yeDMiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9hX2NuLW5vcnRoLTRkIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZGF5dV9kbG1fY2x1c3RlciIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Vjc19hYzciLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9jY2VfbWNwX3RoYWkiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9jb21wYXNzIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZWRzIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfc2VydmljZXN0YWdlX21ncl9kdG0iLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9hX2NuLW5vcnRoLTRmIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfb2EiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9jcGgiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9nYSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX3JtcyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX3Ntbl9hcHBsaWNhdGlvbiIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2dlaXAiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9vcmdhbml6YXRpb25zIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZWNzX2dwdV9nNXIiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF93a3Nfa3AiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9yaV9kd3MiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9hYWRfYmV0YV9pZGMiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9jc2JzX3JlcF9hY2NlbGVyYXRpb24iLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF91Y3MtaW50bCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Vjc19kaXNrQWNjIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZHNzX21vbnRoIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfb2JzX2RlZXBfYXJjaGl2ZSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2NzZyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2RlY19tb250aF91c2VyIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfaWVmX2VkZ2VhdXRvbm9teSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX3ZpcF9iYW5kd2lkdGgiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3Nfb2xkX3Jlb3VyY2UiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF93ZWxpbmticmlkZ2VfZW5kcG9pbnRfYnV5IiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZWNzX3RoaXJkX2ltYWdlIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfcHN0bl9lbmRwb2ludF9idXkiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9tYXBfb2NyIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZGx2X29wZW5fYmV0YSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX29ic19kdWFsc3RhY2siLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lZGNtIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfY3Nic19yZXN0b3JlIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfaXZzY3MiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3NfYzZhIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfdnBuX3ZndyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX3Ntbl9jYWxsbm90aWZ5IiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfb3BfZ2F0ZWRfbGFrZWZvcm1hdGlvbl9iZXQiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9jc2JzX3Byb2dyZXNzYmFyIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZ2FfY24iLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9pZHRfZG1lIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZWNzX29mZmxpbmVfYWM3IiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZXZzX3Bvb2xfY2EiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3Nfb2ZmbGluZV9kaXNrXzQiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9pbnRsX2NvbXBhc3MiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lcHMiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9jc2JzX3Jlc3RvcmVfYWxsIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZmNzX3BheSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2FfYXAtc291dGhlYXN0LTFlIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfYV9ydS1tb3Njb3ctMWIiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9hX2FwLXNvdXRoZWFzdC0xZCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2FfYXAtc291dGhlYXN0LTFmIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfcmFtIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfb3BfZ2F0ZWRfbWVzc2FnZW92ZXI1ZyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Vjc19jNyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2djYiIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX21hcF92aXNpb24iLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3NfcmkiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF91Y3Nfb25wcmVtaXNlcyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2FfcnUtbm9ydGh3ZXN0LTJjIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfcmFtX2ludGwiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9pZWZfcGxhdGludW0iLCJpZCI6IjAifV0sInByb2plY3QiOnsiZG9tYWluIjp7Im5hbWUiOiJzaGVuY2hhbmcyMDAwMjM4MiIsImlkIjoiZDlkZjZlM2Y0NjYxNDJkY2EyMWU5ZDY2MDFlOTYzMzcifSwibmFtZSI6ImNuLW5vcnRoLTQiLCJpZCI6ImZkZGU2OTg3MDJlMjQ3M2Y4ZjEyZDdjNDgxYmJiZTVlIn0sImlzc3VlZF9hdCI6IjIwMjMtMDEtMTRUMTA6NDk6NDkuMjQ3MDAwWiIsInVzZXIiOnsiZG9tYWluIjp7Im5hbWUiOiJzaGVuY2hhbmcyMDAwMjM4MiIsImlkIjoiZDlkZjZlM2Y0NjYxNDJkY2EyMWU5ZDY2MDFlOTYzMzcifSwibmFtZSI6InNjZmFjZTEiLCJwYXNzd29yZF9leHBpcmVzX2F0IjoiIiwiaWQiOiJiMzdjNGY3YzQxODQ0MDkyYTg3OGI4NGEzNzgzNDhkYyJ9fX0xggHBMIIBvQIBATCBlzCBiTELMAkGA1UEBhMCQ04xEjAQBgNVBAgMCUd1YW5nRG9uZzERMA8GA1UEBwwIU2hlblpoZW4xLjAsBgNVBAoMJUh1YXdlaSBTb2Z0d2FyZSBUZWNobm9sb2dpZXMgQ28uLCBMdGQxDjAMBgNVBAsMBUNsb3VkMRMwEQYDVQQDDApjYS5pYW0ucGtpAgkA3LMrXRBhahAwCwYJYIZIAWUDBAIBMA0GCSqGSIb3DQEBAQUABIIBAF3wUVoZW95mrnJALTcyb9F50LkUll14FHMHB8DD5gHIqJ7oAvQFgci0ol3nSJwr6mHCGRVRFnMFqOBn4aiW2NQpygjmmPl1MmvwpjrMmKXNoxWhJ2+WXeBDuv7syN4Oy2i6dd+kDGJ4NUz+xizl5LvylQz9S1THmtraxlyjXnwpSh7GWtXjnaaQ1tGW0QVIBu4xcP0RLHiKMs0+wtLsMYA7ADVCegeICntc+OzsxNCDkmqqMXPX7bbFDiRHeeOEOMeHK3HL3P2gUWEmnSvDMFlPOkNV6YaKvuxgZLVd2AT0jmPDAONGDWEfmKyhwcQjZKI9Uf8qOSb+ntj7vx39mCo='
headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
face_set_name = 'facelib'


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


'''
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
'''


def check_duplicate(model_name, field_name):
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            form = request.POST
            for k, v in form.items():
                if not v:
                    kwargs['err_message'] = f'{k} 不能为空'
                    break
            model = apps.get_model('app1', model_name)
            if model.objects.filter(**{field_name: form.get(field_name)}).exists():
                kwargs['err_message'] = f'{field_name} 已经存在'
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return _decorator


def check_permission(user, permission_name, user_type):
    if user_type == 'student':
        return models.Stu_Auth.objects.filter(studentNo=user, authName=permission_name).exists()
    elif user_type == 'teacher':
        return models.Tea_Auth.objects.filter(teacherNo=user, authName=permission_name).exists()
        # return models.Tea_Auth.objects.filter(teacherNo_id=user, authName=permission_name).exists()
    return False


# 装饰器检查用户权限
def permission_required(permission_name, user_type):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not check_permission(request.get_signed_cookie("username", salt="dsb"), permission_name, user_type):
                # 权限不足，弹出提示窗口
                return render(request, 'error.html', {"errmsg": "您没有该权限！"})
                # return JsonResponse({'error': 'Permission denied'})
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


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
    i = Image.open(img)
    imgSize = i.size
    n = imgSize[0] / imgSize[1]
    width = 300
    length = int(300 * n)
    resized_image = i.resize((length, width), Image.LANCZOS)
    resized_image.save('temp.jpg')
    rep = redirect('/student')
    rep.set_signed_cookie("is_login", "1", salt="dsb", max_age=60 * 60 * 24 * 7)
    rep.set_signed_cookie("username", studentNo, salt="dsb", max_age=60 * 60 * 24 * 7)
    models.Stu_Auth.objects.create(authNo=7, studentNo=studentNo,authName='增选课程stu')
    models.Student.objects.create(studentNo=studentNo, name=user, password=pwd, photo=img, img_name=img.name)
    url = "https://{endpoint}/v2/{project_id}/face-sets/{face_set_name}/faces".format(endpoint=endpoint,
                                                                                      project_id=project_id,
                                                                                      face_set_name=face_set_name)
    imagepath = 'temp.jpg'
    with open(imagepath, "rb") as bin_data:
        image_data = bin_data.read()
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    body = {
        "image_base64": image_base64,
        "external_image_id": "imageID",
        "external_fields": {
            "timestamp": 12,
            "id": "home"
        }
    }
    response = requests.post(url, headers=headers, json=body, verify=False)
    print(response.text)
    path = 'temp.jpg'
    os.remove(path)
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
    ask = request.GET.get("ask")
    print(ask)
    if ask:
        cursor = connection.cursor()
        sql = "SELECT classNo, courseNo, courseName, grade " \
              "FROM renLianShiBie1.app1_class a, renLianShiBie1.app1_course b " \
              "WHERE a.course_id = b.courseNo AND a.teacher_id = " + teaName + " AND b.courseName like '%" + ask + "%';"
        cursor.execute(sql)
        res = cursor.fetchall()
    else:
        cursor = connection.cursor()
        sql = "SELECT classNo, courseNo, courseName, grade " \
              "FROM renLianShiBie1.app1_class a, renLianShiBie1.app1_course b " \
              "WHERE a.course_id = b.courseNo AND a.teacher_id = " + teaName + ";"
        cursor.execute(sql)
        res = cursor.fetchall()
    return render(request, "Teacher/Tmain.html", {"teaName": teaName, "res": res})


@check_login
def teacourse(request):
    teaName = request.get_signed_cookie("username", salt="dsb")
    classNo = request.GET.get('classNo')
    courseNo = request.GET.get('courseNo')
    ask = request.GET.get('ask')
    courseName = models.Course.objects.filter(courseNo=courseNo).first().courseName
    print(courseName)
    print(classNo)
    cursor = connection.cursor()
    if ask:
        sql = "SELECT studentNo, `name` " \
              "FROM renLianShiBie1.app1_student a, renLianShiBie1.app1_class_students b " \
              "WHERE a.name like '%" + ask + "%' AND a.studentNo = b.student_id AND b.class_id = " + classNo + ";"
    else:
        sql = "SELECT studentNo, `name` " \
              "FROM renLianShiBie1.app1_student a, renLianShiBie1.app1_class_students b " \
              "WHERE a.studentNo = b.student_id AND b.class_id = " + classNo + ";"
    print(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    return render(request, "Teacher/Tcourse.html",
                  {"teaName": teaName, "res": res, "courseName": courseName, "classNo": classNo, "courseNo": courseNo})


@check_login
@permission_required('删除学生tea', 'teacher')
def delstudent(request):
    '''
    tid = request.GET.get('tid')
    sql = "SELECT id FROM tea_auth WHERE " \
            "teacherNo_id = " + tid + "authNo_id = 003"
    cursor = connection.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    if res == None:
        return render()
    '''
    sid = request.GET.get('sid')
    cid = request.GET.get('cid')
    coid = request.GET.get('coid')
    print("1:", sid, cid, coid)
    cursor = connection.cursor()
    sql = "DELETE FROM renLianShiBie1.app1_class_students WHERE student_id = " + sid + ";"
    cursor.execute(sql)
    return redirect("/teacourse?classNo=" + cid + "&courseNo=" + coid)


@check_login
@permission_required('增加学生tea', 'teacher')
def Taddstudent(request):
    teaName = request.get_signed_cookie("username", salt="dsb")
    cid = request.GET.get('cid')
    sid = request.GET.get('sid')
    coid = request.GET.get('coid')
    ask = request.GET.get('ask')
    courseName = models.Course.objects.filter(courseNo=coid).first().courseName
    print("1:", cid, sid, courseName)
    cursor = connection.cursor()
    if sid:
        sql = "INSERT INTO renLianShiBie1.app1_class_students VALUES (null, %s, %s);" % (cid, sid)
        cursor.execute(sql)
    if ask:
        sql = "SELECT studentNo,`name` " \
              "FROM renLianShiBie1.app1_student a " \
              "WHERE a.name like '%" + ask + "%' AND a.studentNo NOT IN " \
                                             "(SELECT student_id FROM renLianShiBie1.app1_class_students b " \
                                             "WHERE b.class_id=" + cid + ");"
        print(sql)
    else:
        sql = "SELECT studentNo,`name` " \
              "FROM renLianShiBie1.app1_student a " \
              "WHERE a.studentNo NOT IN " \
              "(SELECT student_id FROM renLianShiBie1.app1_class_students b " \
              "WHERE b.class_id=%s);" % cid
    cursor.execute(sql)
    res = cursor.fetchall()
    return render(request, "Teacher/add-student.html",
                  {"res": res, "cid": cid, "coid": coid, "courseName": courseName, "teaName": teaName})


@check_login
def classInfo(request):
    data_list = models.Class.objects.all()
    print(data_list)
    return render(request, "Classinfo.html", {"n1": data_list})


@check_login
@permission_required('发布签到tea', 'teacher')
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
    ask = request.GET.get("ask")
    print(Qid)
    if Qid is None:
        return redirect("/teasigninfo/")
    else:
        if ask:
            cursor = connection.cursor()
            sql = "SELECT studentNo, `name`, QTime, status from renLianShiBie1.app1_student a, renLianShiBie1.app1_stuqiandao b " \
                  "where a.studentNo = b.studentNo_id and b.status='已签到' and b.QianDaoId_id= " + Qid + " and a.`name` like '%" + ask + "%';"
            cursor.execute(sql)
            res = cursor.fetchall()
        else:
            cursor = connection.cursor()
            sql = "SELECT studentNo, `name`, QTime, status from renLianShiBie1.app1_student a, renLianShiBie1.app1_stuqiandao b " \
                  "where a.studentNo = b.studentNo_id and b.status='已签到' and b.QianDaoId_id= " + Qid + ";"
            cursor.execute(sql)
            res = cursor.fetchall()
    signcnt = models.StuQianDao.objects.filter(status="已签到", QianDaoId_id=Qid).count()
    unsigncnt = models.StuQianDao.objects.filter(status="未签到", QianDaoId_id=Qid).count()
    teaName = request.get_signed_cookie("username", salt="dsb")
    return render(request, "Teacher/SignResult.html",
                  {"teaName": teaName, "res": res, "Qid": Qid, "signcnt": signcnt, "unsigncnt": unsigncnt})


@check_login
def unsignresult(request):
    Qid = request.GET.get("Qid")
    ask = request.GET.get("ask")
    print(Qid)
    if Qid is None:
        return redirect("/teasigninfo/")
    else:
        if ask:
            cursor = connection.cursor()
            sql = "SELECT studentNo, `name`, QTime, status from renLianShiBie1.app1_student a, renLianShiBie1.app1_stuqiandao b " \
                  "where a.studentNo = b.studentNo_id and b.status='未签到' and b.QianDaoId_id= " + Qid + " and a.`name` like '%" + ask + "%';"
            cursor.execute(sql)
            res = cursor.fetchall()
        else:
            cursor = connection.cursor()
            sql = "SELECT studentNo, `name`, QTime, status from renLianShiBie1.app1_student a, renLianShiBie1.app1_stuqiandao b " \
                  "where a.studentNo = b.studentNo_id and b.status='未签到' and b.QianDaoId_id= " + Qid + ";"
            cursor.execute(sql)
            res = cursor.fetchall()
    signcnt = models.StuQianDao.objects.filter(status="已签到", QianDaoId_id=Qid).count()
    unsigncnt = models.StuQianDao.objects.filter(status="未签到", QianDaoId_id=Qid).count()
    teaName = request.get_signed_cookie("username", salt="dsb")
    return render(request, "Teacher/UnSignResult.html",
                  {"teaName": teaName, "res": res, "Qid": Qid, "signcnt": signcnt, "unsigncnt": unsigncnt})


@check_login
def teasigninfo(request):
    ask = request.GET.get('ask')
    print(ask)
    teaName = request.get_signed_cookie("username", salt="dsb")
    if ask:
        cursor = connection.cursor()
        sql = "SELECT id, qianDaoName, courseName, class1_id, pubtime from renLianShiBie1.app1_qiandao a where " \
              "teacherNo_id=" + teaName + " and courseName like '%" + ask + "%' order by pubtime desc;"
        cursor.execute(sql)
        res = cursor.fetchall()
    else:
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
    models.StuQianDao.objects.filter(studentNo_id=sid).update(QTime=None, status="未签到")
    return redirect("/signresult/?Qid=" + qid)


@check_login
def setsign(request):
    qid = request.GET.get("qid")
    sid = request.GET.get("sid")
    models.StuQianDao.objects.filter(studentNo_id=sid).update(QTime=datetime.datetime.now(), status="已签到")
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
@check_duplicate('Student', 'studentNo')
def addstudent(request, err_message=None):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method == 'GET':
        return render(request, "Manage/add-student.html", {"admName": admName})
    if err_message:
        return render(request, "Manage/add-student.html", {"admName": admName, "err_message": err_message})
    user = request.POST.get("name")
    pwd = request.POST.get("password")
    studentNo = request.POST.get("studentNo")
    img = request.FILES.get('img')
    i = Image.open(img)
    imgSize = i.size
    n = imgSize[0] / imgSize[1]
    width = 300
    length = int(300 * n)
    resized_image = i.resize((length, width), Image.LANCZOS)
    resized_image.save('temp.jpg')
    if img != None:
        img_name = img.name
        models.Stu_Auth.objects.create(authNo=7, studentNo=studentNo,authName='增选课程stu')
        models.Student.objects.create(studentNo=studentNo, name=user, password=pwd, photo=img, img_name=img_name)
        url = "https://{endpoint}/v2/{project_id}/face-sets/{face_set_name}/faces".format(endpoint=endpoint,
                                                                                          project_id=project_id,
                                                                                          face_set_name=face_set_name)
        imagepath = 'temp.jpg'
        with open(imagepath, "rb") as bin_data:
            image_data = bin_data.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        body = {
            "image_base64": image_base64,
            "external_image_id": "imageID",
            "external_fields": {
                "timestamp": 12,
                "id": "home"
            }
        }
        requests.post(url, headers=headers, json=body, verify=False)
        path = 'temp.jpg'
        os.remove(path)
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
def manageStudentModify(request, nid, err_message=None):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method == 'GET':
        studentNo = models.Student.objects.filter(studentNo=nid).first()
        return render(request, "Manage/modify-student.html", {"admName": admName, "n1": studentNo, "nid": nid})
    user = request.POST.get("name")
    pwd = request.POST.get("password")
    studentNo = request.POST.get("studentNo")
    img = request.FILES.get('img')
    i = Image.open(img)
    imgSize = i.size
    n = imgSize[0] / imgSize[1]
    width = 300
    length = int(300 * n)
    resized_image = i.resize((length, width), Image.LANCZOS)
    resized_image.save('temp.jpg')
    if (img != None):
        img_name = img.name
        models.StudentPhoto.objects.create(photo=img)
        models.Student.objects.filter(studentNo=nid).update(studentNo=nid, name=user, password=pwd, photo=img,
                                                            img_name=img_name)
        url = "https://{endpoint}/v2/{project_id}/face-sets/{face_set_name}/faces".format(endpoint=endpoint,
                                                                                          project_id=project_id,
                                                                                          face_set_name=face_set_name)
        imagepath = 'temp.jpg'
        with open(imagepath, "rb") as bin_data:
            image_data = bin_data.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        body = {
            "image_base64": image_base64,
            "external_image_id": "imageID",
            "external_fields": {
                "timestamp": 12,
                "id": "home"
            }
        }
        response = requests.post(url, headers=headers, json=body, verify=False)
        print(response.text)
        path = 'temp.jpg'
        os.remove(path)
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
@check_duplicate('Course', 'courseNo')
def addcourse(request, err_message=None):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method == 'GET':
        return render(request, "Manage/add-course.html", {"admName": admName})
    if err_message:
        return render(request, "Manage/add-course.html", {"admName": admName, "err_message": err_message})
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
        return render(request, "Manage/modify-course.html", {"admName": admName, "n1": studentNo, "nid": nid})
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
@check_duplicate('Teacher', 'teacherNo')
def addteacher(request, err_message=None):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method == 'GET':
        return render(request, "Manage/add-teacher.html", {"admName": admName})
    if err_message:
        return render(request, "Manage/add-teacher.html", {"admName": admName, "err_message": err_message})
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
@check_duplicate('Teacher', 'teacherNo')
def manageTeacherModify(request, nid):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method == 'GET':
        teacherNo = models.Teacher.objects.filter(teacherNo=nid).first()
        return render(request, "Manage/modify-teacher.html", {"admName": admName, "n1": teacherNo, "nid": nid})
    nid = request.POST.get("nid")
    name = request.POST.get("name")
    user = request.POST.get("user")
    password = request.POST.get("password")
    models.Teacher.objects.filter(teacherNo=nid).update(teacherNo=nid, name=name, password=password, user=user)
    return redirect("/manageteacher")


# 管理员开课班

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
@permission_required('增选课程stu',student)
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
    sql = "SELECT  a.id,now()  FROM  renLianShiBie1.app1_qiandao a,renLianShiBie1.app1_class_students b WHERE pubtime <=" \
          " now() AND duetime >= now() and class1_id=" + classNo + " and a.class1_id=b.class_id and student_id =" + stuName
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
    pbase64 = photo[22:]
    classNo = request.POST.get('classNo')
    c = classNo
    url = "https://{endpoint}/v2/{project_id}/face-sets/{face_set_name}/search".format(
        endpoint=endpoint, project_id=project_id, face_set_name=face_set_name)
    image_base64 = pbase64
    body = {"image_base64": image_base64, "sort": [{"timestamp": "asc"}], "return_fields": ["timestamp", "id"],
            "filter": "timestamp:12", "top_n": 1, "threshold": 0.93}
    response = requests.post(url, headers=headers, json=body, verify=False)
    data = response.json()
    result = data.get('faces')
    if result == []:
        print('签到失败')
        return HttpResponse(0)
    elif result != None:
        cursor = connection.cursor()
        sql = "SELECT  a.id,now()  FROM  renLianShiBie1.app1_qiandao a,renLianShiBie1.app1_class_students b WHERE pubtime <=" \
              " now() AND duetime >= now() and class1_id=" + c + " and a.class1_id=b.class_id and student_id =" + stuName
        cursor.execute(sql)
        res = cursor.fetchall()
        sql2 = "insert into renLianShiBie1.app1_stuqiandao(studentNo_id,QianDaoID_id,QTime,status) values (" + stuName + "," + str(
            res[0][0]) + ",'" + str(res[0][1]) + "','已签到')"
        cursor.execute(sql2)
        print('签到成功')
        return HttpResponse(1)


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
    res = json.dumps(photo)
    # classNo=request.GET.get('classNo')
    return HttpResponse(res)


# 教师权限管理界面
@check_login
def authTeacher(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    ask = request.GET.get("ask")
    if (ask != None):
        teacherNo = models.Teacher.objects.filter(name__contains=ask)
        return render(request, "Manage/AuthTeacher.html", {"admName": admName, "n1": teacherNo})
    if (ask == None):
        teacher_list = models.Teacher.objects.all()
        return render(request, "Manage/AuthTeacher.html", {"admName": admName, "n1": teacher_list})

@check_login
def modifyTeacherAuth(request, tNo):
    admName = request.get_signed_cookie("username", salt="dsb")
    auth_list = models.Tea_Auth.objects.all().filter(teacherNo=tNo)
    return render(request, "Manage/AuthTeacherModify.html", {"admName": admName, "n1": auth_list})

@check_login
def addTeacherAuth(request):
    admName = request.get_signed_cookie("username", salt='dsb')
    ask = request.GET.get("ask")
    tid = request.GET.get("tid")
    if (ask != None):
        cursor = connection.cursor()
        sql = "SELECT authNo,`name`" \
              "From renLianShiBie1.app1_authority" \
              "where `name` LIKE '%" + ask + "%' and authNo not " \
                                           "in ( SELECT b.authNo " \
                                           "from  renLianShiBie1.app1_tea_auth a, " \
                                           "renLianShiBie1.app1_authority b " \
                                           "WHERE b.authNo=a.authNo and a.teacherNo=" + tid + " )"
        cursor.execute(sql)
        auth_list = cursor.fetchall()
        return render(request, "Manage/AuthTeacherAdd.html", {"admName": admName, "n1": auth_list,'name':tid})
    if (ask == None):
        cursor = connection.cursor()
        sql = "SELECT authNo,`name` " \
              "From renLianShiBie1.app1_authority " \
              "where authNo not " \
                "in ( SELECT b.authNo " \
                "from  renLianShiBie1.app1_tea_auth a, " \
                "renLianShiBie1.app1_authority b " \
                "WHERE b.authNo=a.authNo and a.teacherNo=" + tid + ")"
        cursor.execute(sql)
        auth_list = cursor.fetchall()
        return render(request, "Manage/AuthTeacherAdd.html", {"admName": admName, "n1": auth_list,'name':tid})

@check_login
def addOneAuthTeacher(request):
    authID = request.GET.get("authId")
    teaNo = request.GET.get("stuNo")
    authname=request.GET.get("name")
    teaAuth = models.Tea_Auth(authNo=authID, teacherNo=teaNo,authName=authname)
    teaAuth.save()
    return redirect("/manage/authteacher/add?tid="+teaNo)


# 学生权限管理
@check_login
def authStudent(request):
    admName = request.get_signed_cookie("username", salt="dsb")
    ask = request.GET.get("ask")
    if (ask != None):
        studentNo = models.Student.objects.filter(name__contains=ask)
        return render(request, "Manage/AuthStudent.html", {"admName": admName, "n1": studentNo})
    if (ask == None):
        student_list = models.Student.objects.all()
        return render(request, "Manage/AuthStudent.html", {"admName": admName, "n1": student_list})
@check_login
def deleteAuthTeacher(request):
    nid = request.GET.get("nid")
    id=request.GET.get("id")
    cursor = connection.cursor()
    sql =  "DELETE FROM renLianShiBie1.app1_tea_auth WHERE " \
    "teacherNo= " + nid + " and  authNo = "+id
    cursor.execute(sql)
    auth_list = cursor.fetchall()
    return redirect("/manageauthteacher/"+nid+"/modify")
@check_login
def modifyStudentAuth(request, sNo):
    admName = request.get_signed_cookie("username", salt="dsb")
    auth_list = models.Stu_Auth.objects.all().filter(studentNo=sNo)
    return render(request, "Manage/AuthStudentModify.html", {"admName": admName, "n1":auth_list})
@check_login
def addStudentAuth(request, err_message=None):
    admName = request.get_signed_cookie("username", salt='dsb')
    ask = request.GET.get("ask")
    nid = request.GET.get("nid")
    if (ask != None):
        cursor = connection.cursor()
        sql = "SELECT b.authNo,`name`" \
                "From renLianShiBie1.app1_authority "\
                "where `name` LIKE '%" + ask + "%' and authNo not " \
                "in ( SELECT b.authNo " \
                "from  renLianShiBie1.app1_stu_auth a, " \
                "renLianShiBie1.app1_authority b " \
                "WHERE b.authNo=a.authNo and a.studentNo=" + nid +" )"
        cursor.execute(sql)
        auth_list = cursor.fetchall()
        return render(request, "Manage/AuthStudentAdd.html", {"admName": admName, "n1": auth_list,'name':nid})
    if (ask == None):
        cursor = connection.cursor()
        sql = "SELECT authNo,`name` " \
              "From renLianShiBie1.app1_authority " \
              "where  authNo not " \
                                           "in ( SELECT b.authNo " \
                                           "from  renLianShiBie1.app1_stu_auth a, " \
                                           "renLianShiBie1.app1_authority b " \
                                           "WHERE b.authNo=a.authNo and a.studentNo=" + nid + " )"
        cursor.execute(sql)
        auth_list = cursor.fetchall()
        return render(request, "Manage/AuthStudentAdd.html", {"admName": admName, "n1": auth_list,'name':nid})

@check_login
def addOneAuthStudent(request):
    authID = request.GET.get("authId")
    stuNo = request.GET.get("teaNo")
    authname=request.GET.get("name")
    stuAuth = models.Stu_Auth(authNo=authID, studentNo=stuNo,authName=authname)
    stuAuth.save()
    return redirect("/manage/authstudent/add?nid="+stuNo)

def deleteAuthStudent(request):
    admName = request.get_signed_cookie("username", salt='dsb')
    ask = request.GET.get("ask")
    nid = request.GET.get("nid")
    id=request.GET.get("id")
    cursor = connection.cursor()
    sql =  "DELETE FROM renLianShiBie1.app1_stu_auth WHERE " \
    "studentNo= " + nid + " and  authNo = "+id
    cursor.execute(sql)
    auth_list = cursor.fetchall()
    return redirect("/manageauthstudent/"+nid+"/modify")