from django.db import models

# Create your models here.
class Teacher(models.Model):
    user = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    teacherNo = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=32)

# 管理员
class Admin(models.Model):
    adminNo = models.CharField(max_length=32, primary_key=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

# 权限
class Authority(models.Model):
    authNo = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=32)

# 学生
class Student(models.Model):
    studentNo = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    photo = models.ImageField(upload_to='photos', default='user1.jpg')
    img_name = models.CharField(max_length=100)

class StudentPhoto(models.Model):
    photo = models.ImageField(upload_to='photos', default='user1.jpg')

# 学生权限联系
class Stu_Auth(models.Model):
    studentNo = models.ForeignKey(Student, on_delete=models.CASCADE)
    authNo = models.ForeignKey(Authority, on_delete=models.CASCADE)

# 教师权限联系
class Tea_Auth(models.Model):
    teacherNo = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    authNo = models.ForeignKey(Authority, on_delete=models.CASCADE)

# 课程
class Course(models.Model):
    courseNo = models.CharField(max_length=32, primary_key=True)
    courseName = models.CharField(max_length=32)
    grade = models.FloatField()

# 开课版
class Class(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # 课程号
    classNo = models.CharField(max_length=32, primary_key=True)  # 课程班号
    students = models.ManyToManyField(Student)

# 签到
class QianDao(models.Model):
    id = models.AutoField(primary_key=True)
    pubtime = models.DateTimeField(auto_now_add=True)
    duetime = models.DateTimeField()
    qianDaoName = models.CharField(max_length=32)
    courseName = models.CharField(max_length=32)
    class1 = models.ForeignKey(Class, on_delete=models.CASCADE)

# 学生-签到联系
class StuQianDao(models.Model):
    studentNo = models.ForeignKey(Student, on_delete=models.CASCADE)
    QianDaoId = models.ForeignKey(QianDao, on_delete=models.CASCADE)
    QTime = models.DateTimeField(auto_now_add=True)


class QianDaoMessage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    time = models.TimeField()









