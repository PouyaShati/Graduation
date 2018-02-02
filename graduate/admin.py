from django.contrib import admin

from .models import Question_Set, Answer_Set, Process_Blueprint
from .models import Student_Task_Blueprint, Task_Blueprint
from .models import Employee_Task_Blueprint, Form_Blueprint, Payment_Blueprint
from .models import User, Student, Employee, Department, Process, Task
from .models import Student_Task, Employee_Task, Form, Payment
# Register your models here.

#admin.site.register(Question_Type)
admin.site.register(Question_Set)
admin.site.register(Answer_Set)
admin.site.register(Process_Blueprint)
admin.site.register(Task_Blueprint)
admin.site.register(Student_Task_Blueprint)
admin.site.register(Employee_Task_Blueprint)
admin.site.register(Form_Blueprint)
admin.site.register(Payment_Blueprint)
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Process)
admin.site.register(Task)
admin.site.register(Student_Task)
admin.site.register(Employee_Task)
admin.site.register(Form)
admin.site.register(Payment)