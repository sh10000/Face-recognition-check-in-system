from django.db import models


# Create your models here.

class mypicture(models.Model):
    user = models.CharField(max_length=64)
    photo = models.ImageField(upload_to='photos', default='user1.jpg')


class student(models.Model):
    studentNo = models.CharField(max_length=20)
    studentName = models.CharField(max_length=60)
    studentPic = models.ImageField(upload_to='studentPic', default='user1.jpg')


class teacher(models.Model):
    teacherNo = models.CharField(max_length=20)
    teacherName = models.CharField(max_length=60)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class lesson(models.Model):

