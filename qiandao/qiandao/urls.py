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
    path("index", views.index),
    path('admin', admin.site.urls),
    path('updateinfo', views.updateinfo),
    path("users/list", views.user_list),
    path("tpl", views.tpl),
    path("login/", views.login),
    path("pic_upload", views.pic_upload),
    path("logout", views.logout),
    path("register",views.register),

#教师页面组
    path("teacher", views.teacher),
    path("signpublish", views.signpublish),
    path("signresult", views.signresult),
    path("tcourse", views.tcourse),
    path("unsignresult",views.unsign),
    path("teasigninfo",views.teasigninfo),

#管理员页面组
    path("manage", views.manageIndex),
    path("manage/ManageTeacher", views.manageTeacher),
    path("manage/ManageStudent", views.manageStudent),
    path("manage/ManageCourse", views.manageCourse),
    #管理员管理学生
    path("managestudent", views.manageStudent),
    path("addstudent", views.addstudent),
    path("manage/student/delete", views.manageStudentDelete),
    path("manage/student/<int:nid>/modify", views.manageStudentModify),
    #管理员管理老师
    path("manageteacher", views.manageTeacher),
    path("addteacher", views.addteacher),
    path("manage/teacher/delete", views.manageTeacherDelete),
    path("manage/teacher/<int:nid>/modify", views.manageTeacherModify),
    #管理员管理课程
    path("managecourse", views.manageCourse),
    path("addcourse", views.addcourse),
    path("manage/course/delete", views.manageCourseDelete),
    path("manage/course/<int:nid>/modify", views.manageCourseModify),


#学生签到页面组
    path("student", views.student),
    path("addstudentcourse", views.addCourse),
    path("addstudentcourselist", views.addCourselist),
    path("sign", views.sign),
    path("signed",views.signed),
    path("signinfo",views.signinfo),

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
    
# 测试
    path("ajaxtest", views.ajaxtest)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

