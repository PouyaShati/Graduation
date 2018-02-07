from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from MyUser.models import MyUser
from .models import Employee
from .forms import EmployeeSignUpForm

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
