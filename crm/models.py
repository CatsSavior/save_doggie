from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Student(models.Model):
    sex_types = (
        ('M', 'Man'),
        ('W', 'Woman')
    )
    name = models.CharField(max_length=30, null=True)
    surname = models.CharField(max_length=30, null=True)
    dadname = models.CharField(max_length=30, null=True)
    email = models.EmailField(null=True)
    description = models.TextField(default="")
    photo = models.FilePathField(upload_to='/static/')
    sex = models.CharField(max_length=1, null=True, choices=sex_types)
    weight = models.FloatField(null=True)
    phone_number = models.CharField(max_length=12, null=True)

    def __str__(self):
        return self.name + " " + self.surname