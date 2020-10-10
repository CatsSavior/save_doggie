from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=30, null=True)
    surname = models.CharField(max_length=30, null=True)
    room = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    description = models.TextField(default="")
    photo = models.FilePathField(null=True)

    def __str__(self):
        return self.name + " " + self.surname


