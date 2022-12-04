from django.db import models


# Create your models here.

class mypicture(models.Model):
    user = models.CharField(max_length=64)
    photo = models.ImageField(upload_to='photos', default='user1.jpg')
