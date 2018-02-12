from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from MyUser.models import MyUser
from .models import Student
from Student.forms import StudentSignUpForm, StudentPerformPaymentForm, StudentFillFormForm
from django.contrib.auth import authenticate, login, logout
from django.forms import formset_factory
from django.core.exceptions import ObjectDoesNotExist


from Process.models import Process_Blueprint, Process, Task, Employee_Task_Blueprint, Form_Blueprint, Payment_Blueprint, Employee_Task, Form, Payment, Answer_Set, Answer
# Create your views here.


def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST, request.FILES)
        if form.is_valid(): # TODO what does this is_valid() condition mean? if the form is invalid we cant be able to signup
            user = MyUser.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], # TODO what does this cleaned_data property mean? it returns form data
                                              user_type=MyUser.STUDENTUSER)
            user.save()
            student = Student(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                              email=form.cleaned_data['email'], phone_number=form.cleaned_data['phone_number'],
                              student_id=form.cleaned_data['student_id'],
                              major=form.cleaned_data['major'],
                              document=form.cleaned_data['document'])   # Shouldn't we set the value of account_confirmed as well?

            student.user = user

            student.save()
            for process_bp in Process_Blueprint.objects.all():
                process = Process(instance_of=process_bp, owner=student)
                process.save()
                for task_bp in process_bp.employee_task_bp_defaults.all():
                    task = Employee_Task(process=process, instance_of=task_bp)
                    task.save()
                for task_bp in process_bp.form_bp_defaults.all():
                    task = Form(process=process, instance_of=task_bp)
                    task.save()
                for task_bp in process_bp.payment_bp_defaults.all():
                    task = Payment(process=process, instance_of=task_bp)
                    task.save()

                    # task.save()
                # process.save()

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
    processes = Process.objects.filter(owner=request.user.Student)
    return render(request, 'Student/student_panel.html',
                  {'student': request.user.Student, 'processes':processes})  # , 'providerProvideRequestForm': provider_provide_request_form })44

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
            if form.is_valid():

                student_payment = Payment.objects.get(task_id=task_id)

                student_payment.paid = student_payment.paid + form['paid']

                if student_payment.paid >= student_payment.instance_of.default_amount:
                    student_payment.done = True

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
            if form_set.is_valid():

                student_form = Form.objects.get(task_id=task_id)

                answer_set = Answer_Set()
                student_form.answer_set = answer_set
                n = int(form_set['form-TOTAL_FORMS'])
                for i in range(0, n):
                    answer = Answer(text=form_set['form-' + str(i) + '-answer'], belongs_to=answer_set)
                    answer.save()
                answer_set.save()

                # TODO add setting the done value

                student_form.save()
                return HttpResponseRedirect('/student/perform_task')
            else:
                return render(request, 'Student/student_fill_form.html', {'fill_form_form_set': form_set})
        else:
            return render(request, 'Student/student_fill_form.html',
                          {'fill_form_form_set': FormSet(label_suffix='')})

def students_list(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.EMPLOYEEUSER and request.user.user_type != MyUser.ADMINUSER:
        return HttpResponseRedirect('/not_eligible')
    students = Student.objects.all()
    return render(request, 'Student/all_students_list.html', {'students': students})

def student_404(request):
    return render(request, 'Student/404.html', status=404)

def perform_process(request, process_blueprint_name): #TODO kar nemikone in
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.STUDENTUSER:
        return HttpResponseRedirect('/not_eligible')

    try:
        process_bp = Process_Blueprint.objects.get(name=process_blueprint_name)
        process = Process.objects.get(owner=request.user.Student, instance_of=process_bp)
        form_tasks = Form.objects.filter(process= process)
        payment_tasks = Payment.objects.filter(process=process)
        # for task in process.form_task_set.all():
        #     if hasattr(task, 'Form'):
        #         form_tasks.append(task)
        #     elif hasattr(task, 'Payment'):
        #         payment_tasks.append(task)


        #tasks = Process.objects.values_list('defaults', flat=True)
        #payment_tasks = Payment.objects.filter(instance_of__default_of=process_bp)
    except ObjectDoesNotExist:
        message = 'چنین فرایندی وجود ندارد'
        return render(request, 'Process/process_status.html', {'message': message})
    return render(request, 'Process/process_status.html', {'process': process,
                                                                'form_tasks':form_tasks,
                                                                'payment_tasks': payment_tasks}) #TODO this process doesnt exist
