from django.db import models
from MyUser.models import BaseUser

from MyUser.models import MyUser
# Create your models here.

class Student(BaseUser):
    student_id = models.IntegerField()
    graduated = models.BooleanField(default=False)
    major = models.CharField(max_length=20, choices=[
        ('Computer Engineering', 'Computer Engineering'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Mathematics', 'Mathematics'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry')
                              ])