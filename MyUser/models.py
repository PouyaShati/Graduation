from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import RegexValidator

# Create your models here.
class MyUser(AbstractUser):
    STUDENTUSER = 'ST'
    EMPLOYEEUSER = 'EM'
    OPERATORUSER = 'OP'
    # ADMIN = 'AD'
    # SYSTEM = 'SY' What's the purpose of these two?

    user_type = models.CharField(max_length=2, choices=(
        (STUDENTUSER, 'Student'),
        (EMPLOYEEUSER, 'Employee'),
        (OPERATORUSER, 'Operator'),
        # (ADMIN, 'Admin'),
        # (SYSTEM, 'System'),
    ),
    default=STUDENTUSER)


'''
class BaseUser(models.Model): # Should we tweak the max_length parameters according to a common standard?
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='BaseUser')

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, validators=[
        RegexValidator(regex=r'^(\+|00)\d{11,12}$',
        message="Invalid Phone Number")])
    user_name = models.CharField(max_length=30) # Do we need this?
    # password = models.IntegerField(default=0) Do we need this?
    # logged_in = models.BooleanField(default=False) Do we need this?
    account_confirmed = models.BooleanField(default=False) # What's this field's purpose?
'''