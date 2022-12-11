from django.db import models

# Create your models here.
class Teacher(models.Model):
    user = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    teacherNo = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=32)

class Student(models.Model):
    name = models.CharField(max_length=32)
    studentNo = models.CharField(max_length=32, primary_key=True)
    photo = models.ImageField(upload_to='photos', default='user1.jpg')
class Course(models.Model): # 课程
    courseNo = models.CharField(max_length=32, primary_key=True)
    courseName = models.CharField(max_length=32)
    grade = models.FloatField()

class Class(models.Model): # 开课版
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # 课程号
    classNo = models.CharField(max_length=32, primary_key=True) # 课程班号
    students = models.ManyToManyField(Student)
class QianDao(models.Model):
    qianDaoName = models.CharField(max_length=32)
    courseName = models.CharField(max_length=32)
    class1 = models.ForeignKey(Class, on_delete=models.CASCADE)


class QianDaoMessage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    time = models.TimeField()









