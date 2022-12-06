from django.db import models

# Create your models here.
class Teacher(models.Model):
    user = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    teacherNo = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    courseNo = models.CharField(max_length=32)# 所教课程
    classNo = models.CharField(max_length=32)# 开班号

class Student(models.Model):
    name = models.CharField(max_length=32)
    studentNo = models.CharField(max_length=32)
    photo = models.ImageField(upload_to='photos', default='user1.jpg')

class Course(models.Model): # 课程
    courseNo = models.CharField(max_length=32)
    courseName = models.CharField(max_length=32)
    grade = models.FloatField()

class Class(models.Model): # 开课版
    teacherNo = models.CharField(max_length=32)
    courseNo = models.CharField(max_length=32) # 课程号
    classNo = models.CharField(max_length=32) # 课程班号
    studentNo = models.CharField(max_length=32)
    qianDaoSum = models.IntegerField()
class QianDao(models.Model):
    qianDaoName = models.CharField(max_length=32)
    courseNo = models.CharField(max_length=32)


class QianDaoMessage(models.Model):
    studentNo = models.CharField(max_length=32)
    time = models.TimeField()


