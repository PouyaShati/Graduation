from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from MyUser.models import MyUser
from .models import Student
from Student.forms import StudentSignUpForm, StudentPerformPaymentForm, StudentFillFormForm
from django.contrib.auth import authenticate, login, logout
from django.forms import formset_factory


from Process.models import Process_Blueprint, Process, Task, Employee_Task_Blueprint, Form_Blueprint, Payment_Blueprint, Employee_Task, Form, Payment, Answer_Set, Answer
# Create your views here.


def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid(): # TODO what does this is_valid() condition mean? if the form is invalid we cant be able to signup
            user = MyUser.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], # TODO what does this cleaned_data property mean? it returns form data
                                              user_type=MyUser.STUDENTUSER)
            user.save()
            student = Student(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                              email=form.cleaned_data['email'], phone_number=form.cleaned_data['phone_number'],
                              student_id=form.cleaned_data['student_id'],
                              major=form.cleaned_data['major'])  # Shouldn't we set the value of account_confirmed as well?

            student.user = user

            student.save()
            for process_bp in Process_Blueprint.objects.all():
                process = Process(instance_of=process_bp, owner=student)
                for task_bp in process_bp.defaults.all():
                    if hasattr(task_bp, 'Employee_Task_Blueprint'):
                        task = Employee_Task(process=process, instance_of=task_bp)
                    elif hasattr(task_bp, 'Form_Blueprint'):
                        task = Form(process=process, instance_of=task_bp)
                    elif hasattr(task_bp, 'Payment_Blueprint'):
                        task = Payment(process=process, instance_of=task_bp)
                    task.save()
                process.save()

            return HttpResponseRedirect('/user/login')
        else:

            return render(request, 'Student/student_signup.html', {'signup_form': form})
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
            return HttpResponseRedirect('/student/panel')
        else:
            message = 'نام کاربری یا رمز عبور اشتباه است'
            return render(request, 'Student/student_login.html', {'message': message},status=403)


def student_logout(request):
    logout(request)
    return HttpResponseRedirect('/user/login')


def student_panel(request): #, action):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.STUDENTUSER:
        return HttpResponseRedirect('/user/login')

    return render(request, 'Student/student_panel.html',
                  {'student': request.user.Student})  # , 'providerProvideRequestForm': provider_provide_request_form })44

def perform_task(request, task_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.STUDENTUSER:
        return HttpResponseRedirect('/user/login')
    if hasattr(Task.objects.get(task_id=task_id), 'Employee_Task'):
        return HttpResponseRedirect('/')

    if hasattr(Task.objects.get(task_id=task_id), 'Payment'):
        if request.method == 'POST':
            form = StudentPerformPaymentForm(request.POST)
            if form.is_valid(): # TODO what does this is_valid() condition mean?

                student_payment = Payment.objects.get(task_id=task_id)

                student_payment.paid = student_payment.paid + form['paid']

                student_payment.save()
                return HttpResponseRedirect('/student/perform_task')
            else:
                return render(request, 'Student/student_perform_payment.html', {'perform_payment_form': form})
        else:
            return render(request, 'Student/student_perform_payment.html', {'perform_payment_form': StudentPerformPaymentForm(label_suffix='')})

    elif hasattr(Task.objects.get(task_id=task_id), 'Form'):
        FormSet = formset_factory(StudentFillFormForm)
        if request.method == 'POST':
            form_set = FormSet(request.POST)
            if form_set.is_valid():  # TODO what does this is_valid() condition mean?

                student_form = Form.objects.get(task_id=task_id)

                answer_set = Answer_Set()
                student_form.answer_set = answer_set
                n = int(form_set['form-TOTAL_FORMS'])
                for i in range(0, n):
                    answer = Answer(text=form_set['form-' + str(i) + '-answer'], belongs_to=answer_set)
                    answer.save()
                answer_set.save()

                student_form.save()
                return HttpResponseRedirect('/student/perform_task')
            else:
                return render(request, 'Student/student_fill_form.html', {'fill_form_form_set': form_set})
        else:
            return render(request, 'Student/student_fill_form.html',
                          {'fill_form_form_set': FormSet(label_suffix='')})

def students_list(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/not_logged_in')
    if request.user.user_type != MyUser.EMPLOYEEUSER and request.user.user_type != MyUser.ADMINUSER:
        return HttpResponseRedirect('/not_eligible')
    students = Student.objects.all()
    return render(request, 'Student/all_students_list.html', {'students': students})

def student_404(request):
    return render(request, 'Student/404.html')