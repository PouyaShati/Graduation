from django.db import models
from Student.models import Student
from Employee.models import Department
from django.utils import timezone
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Question_Set(models.Model):
    name = models.CharField(max_length=60, null=True)
    def __str__(self):
        return str(self.name)

class Answer_Set (models.Model):
    name = models.CharField(max_length=60, null=True)

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    text = models.CharField(max_length=1000)
    type = models.CharField(max_length=20, choices=[
        ('Text','Text'),
        ('Integer','Integer'),
        ('Real','Real'),
        ('Document','Document'),
        ('Multiple Choice','Multiple Choice'),])
    belongs_to = models.ForeignKey(Question_Set, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.text)

class Answer(models.Model):
    text = models.CharField(max_length=1000)
    belongs_to = models.ForeignKey(Answer_Set, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.text)





class Task_Blueprint(models.Model):
    name = models.CharField(max_length=60)
    # default_of = models.ForeignKey(Process_Blueprint, on_delete=models.CASCADE, null=True, blank=True) #TODO what is default of? null=True ro man gozashtam

    def __str__(self):
        return str(self.name)
    # TODO Add processes that get invalidate after failing to validate this one

class Student_Task_Blueprint(Task_Blueprint):
    is_timed = models.BooleanField(default=False)
    max_time = models.DateTimeField(default=timezone.ZERO, null=True, blank=True)

class Employee_Task_Blueprint(Task_Blueprint):
    question_set = models.ForeignKey(Question_Set, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.name)

class Form_Blueprint(Student_Task_Blueprint):
    question_set = models.ForeignKey(Question_Set, on_delete=models.CASCADE, null=True)

class Payment_Blueprint(Student_Task_Blueprint):
    receiver = models.IntegerField(default=0) #TODO add this to form
    default_amount = models.IntegerField(null=True)


class Process_Blueprint(models.Model):
    name = models.CharField(max_length=60)
    preprocesses = models.ManyToManyField('self')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    employee_task_bp_defaults = models.ManyToManyField(Employee_Task_Blueprint)
    form_bp_defaults = models.ManyToManyField(Form_Blueprint)
    payment_bp_defaults = models.ManyToManyField(Payment_Blueprint)



class Process(models.Model):
    # validated = models.BooleanField(default=False) do we need this?
    instance_of = models.ForeignKey(Process_Blueprint, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

class Task(models.Model):
    done = models.BooleanField(default=False)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, null=True)
    task_id = models.AutoField(primary_key=True)

class Student_Task(Task):
    start_time = models.DateTimeField(default=datetime.now(), null=True)

class Employee_Task(Task):
    answer_set = models.OneToOneField(Answer_Set, on_delete=models.CASCADE, null=True)
    instance_of = models.ForeignKey(Employee_Task_Blueprint, on_delete=models.CASCADE, null=True)

class Form(Student_Task):
    answer_set = models.OneToOneField(Answer_Set, on_delete=models.CASCADE, null=True)
    instance_of = models.ForeignKey(Form_Blueprint, on_delete=models.CASCADE, null=True)

class Payment(Student_Task):
    paid = models.IntegerField(default=0)
    instance_of = models.ForeignKey(Payment_Blueprint, on_delete=models.CASCADE, null=True)
