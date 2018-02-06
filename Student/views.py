from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from MyUser.models import MyUser
from .models import Student
from Student.forms import StudentSignUpForm
from django.contrib.auth import authenticate, login, logout
#from Process.models import Process_Blueprint, Process, Task, Employee_Task_Blueprint, Form_Blueprint, Payment_Blueprint, Employee_Task, Form, Payment
# Create your views here.


def student_signup(request):
    if request.method == 'POST':
        form = request.POST
        user = MyUser.objects.create_user(username=form['username'], password=form['password1'], # why "password1" and not just "password" ?
                                        user_type=MyUser.STUDENTUSER)
        user.save()
        student = Student(first_name=form['first_name'], last_name=form['last_name'],
                          email=form['email'], phone_number=form['phone_number'],
                          student_id=form['student_id'], major=form['major']) # Shouldn't we set the value of account_confirmed as well?

        student.user = user
        '''
        for process_bp in Process_Blueprint.objects.all():
            process = Process(instance_of=process_bp, owner=student)
            for task_bp in process_bp.task_blueprint_set:
                if hasattr(task_bp, 'Employee_Task_Blueprint'):
                    task = Employee_Task(process=process, instance_of=task_bp)
                elif hasattr(task_bp, 'Form_Blueprint'):
                    task = Form(process=process, instance_of=task_bp)
                elif hasattr(task_bp, 'Payment_Blueprint'):
                    task = Payment(process=process, instance_of=task_bp)

                task.save()
            process.save()
        '''
        student.save()

        return HttpResponseRedirect('/student/student_login')
    else:
        return render(request, 'Student/student_signup.html', {'signup_form': StudentSignUpForm(label_suffix='')})



def student_login(request):
    if request.method == 'GET':
        return render(request, 'Student/student_login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if (user is not None) and (user.user_type == MyUser.STUDENTUSER):
            login(request, user)
            return HttpResponseRedirect('/student/student_panel')
        else:
            return render(request, 'Student/student_login.html', status=403)


def student_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def student_panel(request, action=''):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/Student/student_login')
    if request.user.user_type != MyUser.STUDENTUSER:
        return HttpResponseRedirect('/Student/student_login')

    ''' do we need all this?
    if action == 'provider_provide_request':
        if request.method == 'GET':
            form = ProviderProvideRequestForm(label_suffix='')
            return render(request, 'Provider/provider_panel_form.html', {'form': form})
        else:
            form = ProviderProvideRequestForm(request.POST, request.FILES)
            provider_provide_request = form.save(commit=False)
            provider_provide_request.provider = request.user.provider
            provider_provide_request.save()
            return HttpResponseRedirect('/providers/provider_panel')
    provider_provide_request_form = ProviderProvideRequestForm(label_suffix='')
    '''

    return render(request, 'Student/student_panel.html',
                  {'student': request.user.Student}) # , 'providerProvideRequestForm': provider_provide_request_form })44