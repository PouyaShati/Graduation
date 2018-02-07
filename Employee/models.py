from django.db import models
#from MyUser.models import BaseUser
from django.core.validators import RegexValidator

from MyUser.models import MyUser
# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='Employee')
    employee_id = models.IntegerField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, validators=[
        RegexValidator(regex=r'^((\+|00)\d{11,12})|(09\d{9})$',
        message="Invalid Phone Number")])
    user_name = models.CharField(max_length=30) # Do we need this?
    # password = models.IntegerField(default=0) Do we need this?
    # logged_in = models.BooleanField(default=False) Do we need this?
    account_confirmed = models.BooleanField(default=False) # What's this field's purpose?