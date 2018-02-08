from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from MyUser.models import MyUser
from .models import Employee, Department
from .forms import EmployeeSignUpForm, AddDepartmentForm, EmployForm, FireForm, SetManagerForm, EmployeePerformTaskForm, AddTaskForm
from Process.models import Task, Employee_Task, Employee_Task_Blueprint, Form_Blueprint
from Process.models import Payment_Blueprint, Form, Payment, Task_Blueprint, Process_Blueprint, Process
from Student.models import Student

# Create your views here.
def employee_signup(request):
    if request.method == 'POST':
        form = EmployeeSignUpForm(request.POST)
        if form.is_valid(): # TODO what does this is_valid() condition mean?
            user = MyUser.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], # TODO what does this cleaned_data property mean?
                                              user_type=MyUser.EMPLOYEEUSER)
            user.save()
            employee = Employee(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                              email=form.cleaned_data['email'], phone_number=form.cleaned_data['phone_number'],
                              employee_id=form.cleaned_data['employee_id'])  # Shouldn't we set the value of account_confirmed as well?

            employee.user = user

            employee.save()
            return HttpResponseRedirect('/employee/employee_login')
        else:

            return render(request, 'Employee/employee_signup.html', {'signup_form': form})
    else:
        return render(request, 'Employee/employee_signup.html', {'signup_form': EmployeeSignUpForm(label_suffix='')})


def employee_login(request):
    if request.method == 'GET':
        return render(request, 'Employee/employee_login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if (user is not None) and (user.user_type == MyUser.EMPLOYEEUSER):
            login(request, user)
            return HttpResponseRedirect('/employee/employee_panel')
        else:
            return render(request, 'Employee/employee_login.html', status=403)


def employee_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def employee_panel(request): #, action):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/Employee/employee_login')
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        return HttpResponseRedirect('/Employee/employee_login')

    return render(request, 'Employee/employee_panel.html',
                  {
                      'employee': request.user.Employee})


def add_department(request):
    if request.method == 'GET':
        return render(request, 'Employee/add_department.html', {'add_department_form': AddDepartmentForm(label_suffix='')})
    else:
        form = AddDepartmentForm(request.POST)
        department = Department(name=form['name'], department_id=form['department_id'])
        department.save()
        return HttpResponseRedirect('/department_panel/' + department.department_id)



def department_panel(request, department_id, action):
    department = Department.objects.get(department_id=department_id)
    if action == 'employ':
        if request.method == 'POST':
            form = request.POST
            employee = Employee.objects.get(employee_id=form['employee_id'])
            employee.works_in = department
            employee.save()
            return HttpResponseRedirect('/employee/department_panel/' + department_id)
        else:
            form = EmployForm(label_suffix='')
            return render(request, 'Employee/employ.html', {'form': form})

    elif action == 'fire':
        if request.method == 'POST':
            form = request.POST
            employee = Employee.objects.get(employee_id=form['employee_id'])
            employee.works_in = None
            employee.save()
            return HttpResponseRedirect('/employee/department_panel/' + department_id)
        else:
            form = FireForm(label_suffix='')
            return render(request, 'Employee/fire.html', {'form': form})

    elif action == 'set_manager':
        if request.method == 'POST':
            form = request.POST
            employee = Employee.objects.get(employee_id=form['employee_id'])
            department.manager = employee
            department.save()
            return HttpResponseRedirect('/employee/department_panel/' + department_id)
        else:
            form = SetManagerForm(label_suffix='')
            return render(request, 'Employee/set_manager.html', {'form': form})

    else:
        if request.method == 'POST':
            return HttpResponseRedirect('/')
        else:
            return render(request, 'Process/department_panel.html', {'department': department})




def perform_task(request, task_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/student/login')
    if request.user.user_type != MyUser.STUDENTUSER:
        return HttpResponseRedirect('/student/login')
    if hasattr(Task.objects.get(task_id=task_id), 'Form'):
        return HttpResponseRedirect('/')
    if hasattr(Task.objects.get(task_id=task_id), 'Payment'):
        return HttpResponseRedirect('/')

    if hasattr(Task.objects.get(task_id=task_id), 'Form'):
        if request.method == 'POST':
            form = EmployeePerformTaskForm(request.POST)
            if form.is_valid(): # TODO what does this is_valid() condition mean?

                employee_task = Employee_Task.objects.get(task_id=task_id)

                # employee_task.paid = employee_task.paid + form['paid'] # TODO find a way to retrieve all the answers from form

                employee_task.save()
                return HttpResponseRedirect('/employee/perform_task')
            else:
                return render(request, 'Employee/employee_perform_task.html', {'perform_employee_task_form': form})
        else:
            return render(request, 'Employee/employee_perform_task.html', {'perform_employee_task_form': EmployeePerformTaskForm(label_suffix='')})




def add_task(request, task_bp_name):
    if request.method == 'GET':
        return render(request, 'Employee/add_task.html', {'add_task': AddTaskForm(label_suffix='')})
    else:
        form = AddTaskForm(request.POST)
        task_bp = Task_Blueprint.objects.get(name=task_bp_name)
        process_bp = Process_Blueprint.objects.get(name=form['process_bp'])
        student = Student.objects.get(student_id=form['student_id'])
        process = Process.objects.get(instance_of=process_bp, owner=student)

        if hasattr(task_bp, 'Employee_Task_Blueprint'):
            child_bp = Employee_Task_Blueprint.objects.get(name=task_bp_name)
            task = Employee_Task(instance_of=child_bp, process=process)
        elif hasattr(task_bp, 'Form_Blueprint'):
            child_bp = Form_Blueprint.objects.get(name=task_bp_name)
            task = Form(instance_of=child_bp, process=process)
        elif hasattr(task_bp, 'Payment_Blueprint'):
            child_bp = Payment_Blueprint.objects.get(name=task_bp_name)
            task = Payment(instance_of=child_bp, process=process)

        task.save()
        return HttpResponseRedirect('/add_task/'+ task_bp_name)