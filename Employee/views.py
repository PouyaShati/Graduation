from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from MyUser.models import MyUser
from .models import Employee, Department
from .forms import EmployeeSignUpForm, AddDepartmentForm, EmployForm, FireForm, SetManagerForm, EmployeePerformTaskForm, \
    AddTaskForm
from Process.models import Task, Employee_Task, Employee_Task_Blueprint, Form_Blueprint, Answer, Answer_Set
from Process.models import Payment_Blueprint, Form, Payment, Task_Blueprint, Process_Blueprint, Process
from Student.models import Student
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory

# Create your views here.


not_allowed_error = "شما اجازه‌ی ورود به این بخش را ندارید."
not_authenticated_error = "ابتدا وارد شوید."
no_department_error = "چنین دپارتمانی وجود ندارد."
not_manager_error = "شما مدیر هیج دپارتمانی نیستید."


def employee_signup(request):
    if request.method == 'POST':
        form = EmployeeSignUpForm(request.POST)
        if form.is_valid():  # TODO what does this is_valid() condition mean?
            user = MyUser.objects.create_user(username=form.cleaned_data['username'],
                                              password=form.cleaned_data['password1'],
                                              # TODO what does this cleaned_data property mean?
                                              user_type=MyUser.EMPLOYEEUSER)
            user.save()
            employee = Employee(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                                email=form.cleaned_data['email'], phone_number=form.cleaned_data['phone_number'],
                                employee_id=form.cleaned_data[
                                    'employee_id'])  # Shouldn't we set the value of account_confirmed as well?

            employee.user = user

            employee.save()
            return HttpResponseRedirect('/user/login')
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
            return HttpResponseRedirect('/employee/panel')
        else:
            message = 'نام کاربری یا رمز عبور اشتباه است'
            return render(request, 'Employee/employee_login.html', {'message': message}, status=403)


def employee_logout(request):
    logout(request)
    return HttpResponseRedirect('/user/login')


def employee_panel(request):  # , action):
    if not request.user.is_authenticated():
        message = not_authenticated_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        message = not_allowed_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})
    try:
        department = Department.objects.get(manager=request.user.Employee)
        department_url = '/employee/department_panel/' + str(department.department_id)
    except ObjectDoesNotExist:
        department_url = None
    return render(request, 'Employee/employee_panel.html',
                  {'employee': request.user.Employee, 'department_url': department_url})


def add_department(request):
    if not request.user.is_authenticated():
        message = not_authenticated_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})
    if request.user.user_type != MyUser.ADMINUSER:
        message = not_allowed_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})

    if request.method == 'GET':
        return render(request, 'Employee/add_department.html',
                      {'add_department_form': AddDepartmentForm(label_suffix='')})
    else:
        form = AddDepartmentForm(request.POST)
        if form.is_valid():
            department = Department(name=form.cleaned_data['name'], department_id=form.cleaned_data['department_id'])
            department.save()
            return HttpResponseRedirect('/employee/department_panel/' + str(department.department_id))
        else:
            return render(request, 'Employee/add_department.html', {'add_department_form': form})


def department_panel(request, department_id, action):
    if not request.user.is_authenticated():
        message = not_authenticated_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})
    if request.user.user_type != MyUser.ADMINUSER and request.user.user_type != MyUser.EMPLOYEEUSER:
        message = not_allowed_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})
    if request.user.user_type == MyUser.ADMINUSER:
        base_html = 'base/op_base.html'
    else:
        base_html = 'base/emp_base.html'
    try:
        department = Department.objects.get(department_id=department_id)

        if request.user.user_type != MyUser.ADMINUSER and Employee.objects.get(user=request.user) != department.manager:
            message = not_allowed_error
            return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                       'base_html': 'base/base.html'})
        if action == 'employ':
            if request.method == 'POST':
                form = EmployForm(request.POST)
                if form.is_valid():
                    try:
                        employee = Employee.objects.get(
                            employee_id=form.cleaned_data['employee_id'])
                        employee.works_in = department
                        employee.save()
                        return HttpResponseRedirect('/employee/department_panel/' + department_id)
                    except ObjectDoesNotExist:
                        message = 'چنین کارمندی وجود ندارد'
                        return render(request, 'Employee/employ.html',
                                      {'form': form, 'message': message, 'base_html': base_html})
                else:
                    return render(request, 'Employee/employ.html', {'form': form, 'base_html': base_html})
            else:
                form = EmployForm(label_suffix='')
                return render(request, 'Employee/employ.html', {'form': form, 'base_html': base_html})

        elif action == 'fire':
            if request.method == 'POST':
                form = FireForm(request.POST)
                if form.is_valid():
                    try:
                        employee = Employee.objects.get(
                            employee_id=form.cleaned_data['employee_id'])
                        employee.works_in = None
                        employee.save()
                        return HttpResponseRedirect('/employee/department_panel/' + department_id)
                    except ObjectDoesNotExist:
                        message = 'چنین کارمندی وجود ندارد'
                        return render(request, 'Employee/fire.html',
                                      {'form': form, 'message': message, 'base_html': base_html})
                else:
                    return render(request, 'Employee/fire.html', {'form': form, 'base_html': base_html})
            else:
                form = FireForm(label_suffix='')
                return render(request, 'Employee/fire.html', {'form': form, 'base_html': base_html})

        elif action == 'set_manager':
            if request.method == 'POST':
                form = SetManagerForm(request.POST)
                if form.is_valid():
                    try:
                        employee = Employee.objects.get(
                            employee_id=form.cleaned_data['employee_id'])
                        department.manager = employee
                        department.save()
                        return HttpResponseRedirect('/employee/department_panel/' + department_id)
                    except ObjectDoesNotExist:
                        message = 'چنین کارمندی وجود ندارد'
                        return render(request, 'Employee/set_manager.html',
                                      {'form': form, 'message': message, 'base_html': base_html})
                else:
                    return render(request, 'Employee/set_manager.html', {'form': form, 'base_html': base_html})
            else:
                form = SetManagerForm(label_suffix='')
                return render(request, 'Employee/set_manager.html', {'form': form, 'base_html': base_html})

        else:
            if request.method == 'POST':
                return HttpResponseRedirect('/')
            else:
                employees = Employee.objects.filter(works_in=department)
                return render(request, 'Employee/department_panel.html',
                              {'department': department, 'employees': employees, 'base_html': base_html})
    except ObjectDoesNotExist:
        message = no_department_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})


def perform_task(request, task_id):  # TODO explain this view so i can build templates

    if not request.user.is_authenticated():
        message = not_authenticated_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        message = not_allowed_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})

    task = Task.objects.get(task_id=task_id)

    if hasattr(task, 'Form'):
        return HttpResponseRedirect('/')
    if hasattr(task, 'Payment'):
        return HttpResponseRedirect('/')

    if task.process.instance_of.department != Employee.objects.get(user=request.user).works_in:
        return HttpResponseRedirect('/user/login')

    if hasattr(Task.objects.get(task_id=task_id), 'Employee_Task'):
        FormSet = formset_factory(EmployeePerformTaskForm)
        if request.method == 'POST':
            form_set = FormSet(request.POST)
            if form_set.is_valid():  # TODO what does this is_valid() condition mean?

                employee_task = Employee_Task.objects.get(task_id=task_id)

                answer_set = Answer_Set()
                employee_task.answer_set = answer_set
                n = int(form_set['form-TOTAL_FORMS'])
                for i in range(0, n):
                    answer = Answer(text=form_set['form-' + str(i) + '-answer'], belongs_to=answer_set)
                    answer.save()
                answer_set.save()

                employee_task.save()
                return HttpResponseRedirect('/employee/perform_task')
            else:
                return render(request, 'Employee/employee_perform_task.html',
                              {'perform_employee_task_form_set': form_set})
        else:
            return render(request, 'Employee/employee_perform_task.html',
                          {'perform_employee_task_form_set': FormSet(label_suffix='')})


def add_task(request, task_bp_name):  # TODO explain this view so i can build template
    if not request.user.is_authenticated():
        message = not_authenticated_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        message = not_allowed_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})

    if request.method == 'GET':
        return render(request, 'Employee/add_task.html', {'add_task': AddTaskForm(label_suffix='')})
    else:
        form = AddTaskForm(request.POST)
        process_bp = Process_Blueprint.objects.get(name=form['process_bp'])
        if process_bp.department != Employee.objects.get(user=request.user).works_in:
            return render(request, 'Employee/add_task.html',
                          {'add_task': AddTaskForm(label_suffix=''), 'message': "you don't work in that company"})
        else:
            task_bp = Task_Blueprint.objects.get(name=task_bp_name)
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
            return HttpResponseRedirect('/add_task/' + task_bp_name)


def all_employees_list(request):
    if not request.user.is_authenticated():
        message = not_authenticated_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})
    if request.user.user_type != MyUser.ADMINUSER:
        message = not_allowed_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})
    employees = Employee.objects.all()
    return render(request, 'Employee/all_employees_list.html', {'employees': employees})


def all_departments_list(request):
    if not request.user.is_authenticated():
        message = not_authenticated_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})
    if request.user.user_type != MyUser.ADMINUSER:
        message = not_allowed_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})
    departments = Department.objects.all()
    return render(request, 'Employee/all_departments_list.html', {'departments': departments})


def all_students_list(request):
    if not request.user.is_authenticated():
        message = not_authenticated_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})
    if request.user.user_type != MyUser.ADMINUSER and request.user.user_type != MyUser.EMPLOYEEUSER:
        message = not_allowed_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})
    if request.user.user_type == MyUser.ADMINUSER:
        base_html = 'base/op_base.html'
    else:
        base_html = 'base/emp_base.html'
    students = Student.objects.all()
    return render(request, 'Employee/all_students_list.html', {'studesnts': students, 'base_html': base_html})


def all_process_blueprints_list(request):
    if not request.user.is_authenticated():
        message = not_authenticated_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})
    if request.user.user_type != MyUser.ADMINUSER and request.user.user_type != MyUser.EMPLOYEEUSER:
        message = not_allowed_error
        return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                   'base_html': 'base/base.html'})
    if request.user.user_type == MyUser.ADMINUSER:
        base_html = 'base/op_base.html'
        process_pbs = Process_Blueprint.objects.all()
    else:
        employee = Employee.objects.get(user=request.user)
        base_html = 'base/emp_base.html'
        try:
            department = Department.objects.get(manager=employee)
            process_pbs = Process_Blueprint.objects.filter(department=department)
        except ObjectDoesNotExist:
            message = not_manager_error
            return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                       'base_html': base_html})
        if department is None:
            message = not_manager_error
            return render(request, 'base/not_authenticated.html', {'error_m': message,
                                                                       'base_html': base_html})
    return render(request, 'Employee/all_process_blueprints_list.html',
                  {'process_pbs': process_pbs, 'base_html': base_html})


def employee_404(request):
    return render(request, 'Employee/404.html', status=404)
