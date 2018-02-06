from django.db import models
from Student.models import Student
from django.utils import timezone
# Create your models here.


class Question_Set(models.Model):
    name = models.CharField(max_length=60, null=True)


class Answer_Set (models.Model):
    name = models.CharField(max_length=60, null=True)

class Question(models.Model):
    text = models.CharField(max_length=1000)
    type = models.CharField(max_length=20, choices=[
        ('Text','Text'),
        ('Integer','Integer'),
        ('Real','Real'),
        ('Document','Document'),
        ('Multiple Choice','Multiple Choice'),])
    belongs_to = models.ForeignKey(Question_Set, on_delete=models.CASCADE, default='')

class Answer(models.Model):
    text = models.CharField(max_length=1000)
    belongs_to = models.ForeignKey(Answer_Set, on_delete=models.CASCADE, default='')







class Process_Blueprint(models.Model):
    name = models.CharField(max_length=60)
    # TODO add department
    preprocesses = models.ManyToManyField('self')
    # TODO Add processes that get invalidate after failing to validate this one

class Task_Blueprint(models.Model):
    name = models.CharField(max_length=60)
    default_of = models.ForeignKey(Process_Blueprint, on_delete=models.CASCADE)

class Student_Task_Blueprint(Task_Blueprint):
    is_timed = models.BooleanField(default=False)
    max_time = models.DateTimeField(default=timezone.ZERO)

class Employee_Task_Blueprint(Task_Blueprint):
    question_set = models.ForeignKey(Question_Set, on_delete=models.CASCADE, null=True)

class Form_Blueprint(Student_Task_Blueprint):
    question_set = models.ForeignKey(Question_Set, on_delete=models.CASCADE, null=True)

class Payment_Blueprint(Student_Task_Blueprint):
    receiver = models.IntegerField(default=0)
    default_amount = models.IntegerField(null=True)





class Process(models.Model):
    validated = models.BooleanField(default=False)
    instance_of = models.ForeignKey(Process_Blueprint, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

class Task(models.Model):
    done = models.BooleanField(default=False)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, null=True)

class Student_Task(Task):
    start_time = models.DateTimeField(default=timezone.ZERO)

class Employee_Task(Task):
    answer_set = models.OneToOneField(Answer_Set, on_delete=models.CASCADE, null=True)
    instance_of = models.ForeignKey(Employee_Task_Blueprint, on_delete=models.CASCADE, null=True)

class Form(Student_Task):
    answer_set = models.OneToOneField(Answer_Set, on_delete=models.CASCADE, null=True)
    instance_of = models.ForeignKey(Form_Blueprint, on_delete=models.CASCADE, null=True)

class Payment(Student_Task):
    paid = models.IntegerField(default=0)
    instance_of = models.ForeignKey(Payment_Blueprint, on_delete=models.CASCADE, null=True)
