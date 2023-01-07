"""qiandao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", views.index),
    path("index/", views.index),
    path('admin/', admin.site.urls),
    path('updateinfo/', views.updateinfo),
    path("users/list/", views.user_list),
    path("tpl/", views.tpl),
    path("login/", views.login),
    path("pic_upload", views.pic_upload),
    path("logout", views.logout),
    path("register/",views.register),

#教师页面组
    path("teacher/", views.teacher),
    path("signpublish/", views.signpublish),
    path("signresult/", views.signresult),
    path("tcourse/", views.tcourse),

#管理员页面组
    path("manager/", views.manageIndex),

    path("manageteacher/", views.manageTeacher),
    path("managestudent/", views.manageStudent),
    path("managecourse/", views.manageCourse),

    path("manager/ManageCourse/", views.manageCourse),
    path("manager/student/delete/", views.managerStudentDelete),
    path("manager/student/add/", views.managerStudentAdd),
    path("manager/student/modify/", views.managerStudentModify),


#学生签到页面组
    path("student/", views.student),
    path("sign/", views.sign),
    path("signinfo/",views.signinfo),

    # path("teacher", views.teacher),
    # path("teacher/publishSing", views.publishSign),
    # path("teacher/signResult",),

    # path("manager",),
    # path("manager/manageTeacher"),
    # path("manager/manageStudent"),
    # path("manage/manageCourse"),
    # path("manage/teacherCourse"),

    # path("studentQianDao", views.studentQiandao),
    path("classInfo", views.classInfo),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

