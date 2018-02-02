from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
import enum

# Create your models here.
#class Question_Type(enum.Enum):
#    Text = "TXT"
#    Num_Int = "INT"
#    Num_Real = "REAL"
#    Doc = "DOC"
#    Multiple = "CHOICE"



class Question_Set(models.Model):
    name = models.CharField(max_length=60)

    questions = ArrayField(models.CharField(max_length=1000), size=None)
    question_types = ArrayField(models.CharField(max_length=20, choices=[
        ('Text','Text'),
        ('Integer','Integer'),
        ('Real','Real'),
        ('Document','Document'),
        ('Multiple Choice','Multiple Choice'),]), size=None)

class Answer_Set (models.Model):
    answers = ArrayField(models.CharField(max_length=1000), size=None)




class Process_Blueprint(models.Model):
    name = models.CharField(max_length=60)
    # TODO add department
    preprocesses = models.ManyToManyField('self')
    # TODO add processes that receive new tasks as a result of this process failure to get validated

class Task_Blueprint(models.Model):
    name = models.CharField(max_length=60)
    default_of = models.ForeignKey(Process_Blueprint, on_delete=models.CASCADE)

class Student_Task_Blueprint(Task_Blueprint):
    is_timed = models.BooleanField(default=False)
    max_time = models.DateTimeField(default=timezone.ZERO)

class Employee_Task_Blueprint(Task_Blueprint):
    question_set = models.ForeignKey(Question_Set, on_delete=models.CASCADE)

class Form_Blueprint(Student_Task_Blueprint):
    question_set = models.ForeignKey(Question_Set, on_delete=models.CASCADE)

class Payment_Blueprint(Student_Task_Blueprint):
    receiver = models.IntegerField(default=0)





class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_name = models.CharField(max_length=30)
    password = models.IntegerField(default=0)
    logged_in = models.BooleanField(default=False)
    # TODO implement functions and the process of logging in and out

class Student(User):
    student_id = models.IntegerField(default=0)
    graduated = models.BooleanField(default=False)
    # TODO add student catalogue?
    # TODO add record
    # TODO keep track of all the employees?
    # TODO implement functions

class Employee(User): # TODO redefine structure of User, Manager, Employee, Operator ...
    employee_id = models.IntegerField(default=0)
    # TODO add student catalogue?
    # TODO add record
    ready = models.BooleanField(default=True)
    # TODO implement functions
    operator_authority = models.BooleanField(default=False)
    # TODO all deps, all tasks and all employees?
    works_in = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)


class Department(models.Model):
    department_id = models.IntegerField(default=0)
    manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    # TODO add record
    # TODO implement functions






class Process(models.Model):
    validated = models.BooleanField(default=False)
    # TODO add record
    # TODO implement functions
    instance_of = models.ForeignKey(Process_Blueprint, on_delete=models.CASCADE)
    owner = models.ForeignKey(Student, on_delete=models.CASCADE)

class Task(models.Model):
    done = models.BooleanField(default=False)
    # TODO add record
    # TODO implement functions
    process = models.ForeignKey(Process, on_delete=models.CASCADE)

class Student_Task(Task):
    start_time = models.DateTimeField(default=timezone.ZERO)

class Employee_Task(Task):
    answer_set = models.OneToOneField(Answer_Set, on_delete=models.CASCADE)
    # TODO implement functions
    instance_of = models.ForeignKey(Employee_Task_Blueprint, on_delete=models.CASCADE)

class Form(Student_Task):
    answer_set = models.OneToOneField(Answer_Set, on_delete=models.CASCADE)
    instance_of = models.ForeignKey(Form_Blueprint, on_delete=models.CASCADE)

class Payment(Student_Task):
    amount = models.IntegerField(default=0)
    instance_of = models.ForeignKey(Payment_Blueprint, on_delete=models.CASCADE)
