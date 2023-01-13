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
import app1
import requests
import base64
import os



endpoint = 'face.cn-north-4.myhuaweicloud.com'
project_id = 'fdde698702e2473f8f12d7c481bbbe5e'
token = 'MIITuAYJKoZIhvcNAQcCoIITqTCCE6UCAQExDTALBglghkgBZQMEAgEwghHKBgkqhkiG9w0BBwGgghG7BIIRt3sidG9rZW4iOnsiZXhwaXJlc19hdCI6IjIwMjMtMDEtMTNUMDg6NDg6NTkuNjI4MDAwWiIsIm1ldGhvZHMiOlsicGFzc3dvcmQiXSwiY2F0YWxvZyI6W10sInJvbGVzIjpbeyJuYW1lIjoidGVfYWRtaW4iLCJpZCI6IjAifSx7Im5hbWUiOiJ0ZV9hZ2VuY3kiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3Nfc3BvdF9pbnN0YW5jZSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2l2YXNfdmNyX3ZjYSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2FfY24tc291dGgtNGMiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3Nfa2FlMSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX0tvb1NlYXJjaENPQlQiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9kd3NfcG9jIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfY2JyX2ZpbGUiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3Nfa2MxX3VzZXJfZGVmaW5lZCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX21lZXRpbmdfZW5kcG9pbnRfYnV5IiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfbWFwX25scCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2VnX2NuIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfcmVkaXM2LWdlbmVyaWMtaW50bCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Rjc19kY3MyLWVudGVycHJpc2UiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF92Y3AiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9jdnIiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9tdWx0aV9iaW5kIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfYV9hcC1zb3V0aGVhc3QtM2QiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9wcm9qZWN0X2RlbCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2NlciIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Nlc19yZXNvdXJjZWdyb3VwX3RhZyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2V2c19yZXR5cGUiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9rb29tYXAiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9ldnNfZXNzZDIiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3NfaXIzeCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2FfY24tc291dGh3ZXN0LTJiIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfY3NlX25hY29zIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfdWNzX2NpYSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2h3ZGV2IiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfc2ZzdHVyYm8iLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9odl92ZW5kb3IiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9hX2NuLW5vcnRoLTRlIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfcngzIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfYV9jbi1ub3J0aC00ZCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2RheXVfZGxtX2NsdXN0ZXIiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3NfYWM3IiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfY2NlX21jcF90aGFpIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfY29tcGFzcyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2VkcyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX3NlcnZpY2VzdGFnZV9tZ3JfZHRtIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfYV9jbi1ub3J0aC00ZiIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX29hIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfY3BoIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZ2EiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9ybXMiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9zbW5fYXBwbGljYXRpb24iLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9nZWlwIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfb3JnYW5pemF0aW9ucyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Vjc19ncHVfZzVyIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfd2tzX2twIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfcmlfZHdzIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfYWFkX2JldGFfaWRjIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfY3Nic19yZXBfYWNjZWxlcmF0aW9uIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfdWNzLWludGwiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3NfZGlza0FjYyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Rzc19tb250aCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX29ic19kZWVwX2FyY2hpdmUiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9jc2ciLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9kZWNfbW9udGhfdXNlciIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2llZl9lZGdlYXV0b25vbXkiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF92aXBfYmFuZHdpZHRoIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZWNzX29sZF9yZW91cmNlIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfd2VsaW5rYnJpZGdlX2VuZHBvaW50X2J1eSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Vjc190aGlyZF9pbWFnZSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX3BzdG5fZW5kcG9pbnRfYnV5IiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfbWFwX29jciIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Rsdl9vcGVuX2JldGEiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9vYnNfZHVhbHN0YWNrIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZWRjbSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2NzYnNfcmVzdG9yZSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2l2c2NzIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZWNzX2M2YSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX3Zwbl92Z3ciLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9zbW5fY2FsbG5vdGlmeSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX29wX2dhdGVkX2xha2Vmb3JtYXRpb25fYmV0IiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfY3Nic19wcm9ncmVzc2JhciIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2dhX2NuIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfaWR0X2RtZSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Vjc19vZmZsaW5lX2FjNyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2V2c19wb29sX2NhIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZWNzX29mZmxpbmVfZGlza180IiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfaW50bF9jb21wYXNzIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZXBzIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfY3Nic19yZXN0b3JlX2FsbCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Zjc19wYXkiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9hX2FwLXNvdXRoZWFzdC0xZSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2FfcnUtbW9zY293LTFiIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfYV9hcC1zb3V0aGVhc3QtMWQiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9hX2FwLXNvdXRoZWFzdC0xZiIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX3JhbSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX29wX2dhdGVkX21lc3NhZ2VvdmVyNWciLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3NfYzciLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9nY2IiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9tYXBfdmlzaW9uIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZWNzX3JpIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfdWNzX29ucHJlbWlzZXMiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9hX3J1LW5vcnRod2VzdC0yYyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX3JhbV9pbnRsIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfaWVmX3BsYXRpbnVtIiwiaWQiOiIwIn1dLCJwcm9qZWN0Ijp7ImRvbWFpbiI6eyJuYW1lIjoic2hlbmNoYW5nMjAwMDIzODIiLCJpZCI6ImQ5ZGY2ZTNmNDY2MTQyZGNhMjFlOWQ2NjAxZTk2MzM3In0sIm5hbWUiOiJjbi1ub3J0aC00IiwiaWQiOiJmZGRlNjk4NzAyZTI0NzNmOGYxMmQ3YzQ4MWJiYmU1ZSJ9LCJpc3N1ZWRfYXQiOiIyMDIzLTAxLTEyVDA4OjQ4OjU5LjYyODAwMFoiLCJ1c2VyIjp7ImRvbWFpbiI6eyJuYW1lIjoic2hlbmNoYW5nMjAwMDIzODIiLCJpZCI6ImQ5ZGY2ZTNmNDY2MTQyZGNhMjFlOWQ2NjAxZTk2MzM3In0sIm5hbWUiOiJzY2ZhY2UxIiwicGFzc3dvcmRfZXhwaXJlc19hdCI6IiIsImlkIjoiYjM3YzRmN2M0MTg0NDA5MmE4NzhiODRhMzc4MzQ4ZGMifX19MYIBwTCCAb0CAQEwgZcwgYkxCzAJBgNVBAYTAkNOMRIwEAYDVQQIDAlHdWFuZ0RvbmcxETAPBgNVBAcMCFNoZW5aaGVuMS4wLAYDVQQKDCVIdWF3ZWkgU29mdHdhcmUgVGVjaG5vbG9naWVzIENvLiwgTHRkMQ4wDAYDVQQLDAVDbG91ZDETMBEGA1UEAwwKY2EuaWFtLnBraQIJANyzK10QYWoQMAsGCWCGSAFlAwQCATANBgkqhkiG9w0BAQEFAASCAQAhyGB3mDl-j91OrLT7935Xg-XmPK-fuUgoWZafjRxmokmQ+x5JlVHGGcCYjuSbNOCZEywt94MYPMB26lgNk4qAKeZo-qrj4kv5qHYSlEqbPa-H8FfVXSRTs+hCa5Bfo0ex2fTorbfmZzSyxqYrbhiJps4T-o44iJO0lDVKn5R6Er+3jafFTsD6XXRZSanpH8KGyQvlEbAG-KhNFTfCzplbPLgaF1qy3iYQppZzV6zAsFG+JxQpNVilnI0VD8BT00m2mI+PCwUFDZUU2q7p-R7VBFMY+NII8yKyl2gGV5dOPar3IPa1SRe8KM2mFAF-8JkZ0sH+z1p+cSO66H01Hk-5'
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
    models.Student.objects.create(studentNo=studentNo, name=user, password=pwd, photo=img, img_name=img.name)
    url = "https://{endpoint}/v2/{project_id}/face-sets/{face_set_name}/faces".format(endpoint=endpoint,project_id=project_id,face_set_name=face_set_name)
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
def addstudent(request,err_message=None):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method == 'GET':
        return render(request, "Manage/add-student.html", {"admName": admName})
    if err_message:
        return render(request, "Manage/add-student.html", {"admName": admName,"err_message": err_message})
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
        models.Student.objects.create(studentNo=studentNo, name=user, password=pwd, photo=img, img_name=img_name)
        url = "https://{endpoint}/v2/{project_id}/face-sets/{face_set_name}/faces".format(endpoint=endpoint,project_id=project_id,face_set_name=face_set_name)
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
def manageStudentModify(request, nid,err_message=None):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method == 'GET':
        studentNo = models.Student.objects.filter(studentNo=nid).first()
        return render(request, "Manage/modify-student.html", {"n1": studentNo, "nid": nid})
    user = request.POST.get("name")
    pwd = request.POST.get("password")
    studentNo = request.POST.get("studentNo")
    img = request.FILES.get('img')
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
@check_duplicate('Course', 'courseNo')
def addcourse(request,err_message=None):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method == 'GET':
        return render(request, "Manage/add-course.html",{"admName": admName})
    if err_message:
        return render(request, "Manage/add-course.html", {"admName": admName,"err_message": err_message})
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
@check_duplicate('Teacher', 'teacherNo')
def addteacher(request,err_message=None):
    admName = request.get_signed_cookie("username", salt="dsb")
    if request.method == 'GET':
        return render(request, "Manage/add-teacher.html",{"admName": admName})
    if err_message:
        return render(request, "Manage/add-teacher.html", {"admName": admName,"err_message": err_message})
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
    print(classNo)
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
        sql2 = "insert into renLianShiBie1.app1_stuqiandao(studentNo_id,QianDaoID_id,QTime,status) values (" + stuName + "," + str(res[0][0]) + ",'" + str(res[0][1]) + "','已签到')"
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
