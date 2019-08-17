from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=30, null=True)
    surname = models.CharField(max_length=30, null=True)
    room = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    description = models.TextField(default="")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    photo = models.FilePathField(null=True)

    def __str__(self):
        return self.name + " " + self.surname

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=255, null=True)
    who = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)


