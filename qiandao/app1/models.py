from django.db import models

# Create your models here.
class Teacher(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    
class mypicture(models.Model):
    user = models.CharField(max_length=64)
    photo = models.ImageField(upload_to='photos', default='user1.jpg')
