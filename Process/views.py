from django.shortcuts import render, redirect, reverse
from Process.models import Process_Blueprint, Employee_Task_Blueprint, Question_Set, Question, Form_Blueprint, Payment_Blueprint, Task_Blueprint
from Employee.models import Department, Employee
from django.http.response import HttpResponseRedirect, HttpResponse
from Process.forms import CreateProcessBlueprintForm, CreateQuestionSetForm, AddQuestionForm, AddPreprocessForm, CreateEmployeeTaskBlueprintForm
from Process.forms import CreateFormBlueprintForm, CreatePaymentBlueprintForm, AddDefaultEmployeeTaskForm, AddDefaultFormBlueprintTaskForm, AddDefaultPaymentBlueprintTaskForm
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from MyUser.models import MyUser
# Create your views here.


def create_process_blueprint(request): # TODO handle actions

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        return HttpResponseRedirect('/user/login')

    employee = Employee.objects.get(user= request.user)
    try:
        department = Department.objects.get(manager= employee)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/user/login')
    if department is None:
        return HttpResponseRedirect('/employee/login')

    # if action == 'add_preprocess':
    #     if request.method == 'POST':
    #         form = AddPreprocessForm(request.POST)
    #         if form.is_valid():
    #             try:
    #                 # request.session['preprocesses'] = []
    #
    #                 # n = int(form_set['form-TOTAL_FORMS'])
    #                 # for i in range(0, n):
    #                 #     request.session['preprocesses'].append(form_set['form-' + str(i) + '-name'])
    #
    #                     new_preprocess = form.cleaned_data['name']
    #                     request.session['preprocesses'].append(new_preprocess)
    #
    #                     # ret   urn HttpResponseRedirect('/process/create_process_blueprint')
    #                     successfully_added = ' با موفقیت به عنوان پیشنیاز افزوده شد ' + new_preprocess.name + ' فرایند '
    #                     return render(request, 'Process/add_preprocess.html', {'form': form, 'successfully_added':successfully_added})
    #                     # return render(request, 'Process/create_process_blueprint.html', {'form': CreateProcessBlueprintForm(label_suffix='')})
    #             except ObjectDoesNotExist:
    #                 message = 'چنین فرایندی وجود ندارد'
    #                 return render(request, 'Process/add_preprocess.html', {'form': form, 'message': message})
    #         else:
    #             return render(request, 'Process/add_preprocess.html', {'form': form})
    #     else:
    #         form = AddPreprocessForm(label_suffix='')
    #         request.session['preprocesses'] = []
    #         return render(request, 'Process/add_preprocess.html', {'form': form})
    # elif action == 'add_default_task':
    #     if request.method == 'POST':
    #         form = AddDefaultTaskForm(request.POST)
    #         if form.is_valid():
    #             try:
    #                 default_task = form.cleaned_data['name']
    #                 request.session['default_tasks'].append(default_task)
    #
    #                 successfully_added = ' با موفقیت به عنوان پیشنیاز افزوده شد ' + default_task.name + ' وظیفه '
    #                 return render(request, 'Process/add_default_task.html', {'form': form, 'successfully_added':successfully_added})
    #             except ObjectDoesNotExist:
    #                 message = 'چنین وظیفه‌ای وجود ندارد'
    #                 return render(request, 'Process/add_default_task.html', {'form': form, 'message': message})
    #         else:
    #             return render(request, 'Process/add_default_task.html', {'form': form})
    #     else:
    #         form = AddDefaultTaskForm(label_suffix='')
    #         request.session['default_tasks'] = []
    #         return render(request, 'Process/add_default_task.html', {'form': form})
    # else:
    if request.method == 'GET':

        form = CreateProcessBlueprintForm(label_suffix='')
        return render(request, 'Process/create_process_blueprint.html', {'form': form})
    else:
        form = CreateProcessBlueprintForm(request.POST)
        if form.is_valid():
            try:
                #department = form.cleaned_data['department']
                process_bp = Process_Blueprint(name=form.cleaned_data['name'], department=department)
                # if 'preprocesses' in request.session.keys():
                #     for preprocess in request.session['preprocesses']:
                #         # preprocess = Process_Blueprint.objects.get(name=preprocess_name)
                #         process_bp.preprocesses.add(preprocess)
                #         del request.session['preprocesses']
                #
                # if 'default_tasks' in request.session.keys():
                #     for default_task_name in request.session['default_tasks']:
                #         default_task = Task_Blueprint.objects.get(name=default_task_name)
                #         process_bp.defaults.add(default_task)
                #         del request.session['default_tasks']

                process_bp.save()
                success_message = 'الگوی فرایند با موفقیت ساخته شد'
                # preprocesses = process_bp.preprocesses.all()
                # tasks = process_bp.defaults.all()
                return render(request, 'Process/create_process_blueprint.html', {'form': form, 'success_message':success_message})
            except ObjectDoesNotExist:
                return render(request, 'Process/create_process_blueprint.html', {'form': form})
        else:
            return render(request, 'Process/create_process_blueprint.html', {'form': form})


def process_blueprint_page(request, name, action=''):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        return HttpResponseRedirect('/user/login')

    employee = Employee.objects.get(user= request.user)
    try:
        department = Department.objects.get(manager= employee)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/user/login')
    if department is None:
        return HttpResponseRedirect('/employee/login')
    try:
        process_pb = Process_Blueprint.objects.get(name=name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/'+name+'pox')
    return_link = '/process/process_blueprint_page/'+name
    if action =='add_preprocess':
        if request.method == 'POST':
            form = AddPreprocessForm(request.POST)
            if form.is_valid():
                try:
                    # request.session['preprocesses'] = []

                    # n = int(form_set['form-TOTAL_FORMS'])
                    # for i in range(0, n):
                    #     request.session['preprocesses'].append(form_set['form-' + str(i) + '-name'])

                        new_preprocess = form.cleaned_data['name']
                        # request.session['preprocesses'].append(new_preprocess)
                        process_pb.preprocesses.add(new_preprocess)
                        process_pb.save()
                        # ret   urn HttpResponseRedirect('/process/create_process_blueprint')
                        successfully_added = ' با موفقیت به عنوان پیشنیاز افزوده شد ' + new_preprocess.name + ' فرایند '
                        return render(request, 'Process/add_preprocess.html', {'form': form, 'successfully_added':successfully_added,
                                                                               'return_link': return_link})
                        # return render(request, 'Process/create_process_blueprint.html', {'form': CreateProcessBlueprintForm(label_suffix='')})
                except ObjectDoesNotExist:
                    message = 'چنین فرایندی وجود ندارد'
                    return render(request, 'Process/add_preprocess.html', {'form': form, 'message': message, 'return_link': return_link})
            else:
                return render(request, 'Process/add_preprocess.html', {'form': form, 'return_link': return_link})
        else:
            form = AddPreprocessForm(label_suffix='')
            return render(request, 'Process/add_preprocess.html', {'form': form, 'return_link': return_link})
    elif action == 'add_default_employee_task':
        if request.method == 'POST':
            form = AddDefaultEmployeeTaskForm(request.POST)
            if form.is_valid():
                try:
                    default_task = form.cleaned_data['employee_task_bp_name']
                    # request.session['default_tasks'].append(default_task)
                    process_pb.employee_task_bp_defaults.add(default_task)
                    process_pb.save()
                    successfully_added = ' با موفقیت به عنوان پیشنیاز افزوده شد ' + default_task.name + ' وظیفه '
                    return render(request, 'Process/add_default_task.html', {'form': form, 'successfully_added':successfully_added
                                                                             ,'return_link': return_link})
                except ObjectDoesNotExist:
                    message = 'چنین وظیفه‌ای وجود ندارد'
                    return render(request, 'Process/add_default_task.html', {'form': form, 'message': message, 'return_link': return_link})
            else:
                return render(request, 'Process/add_default_task.html', {'form': form, 'return_link': return_link})
        else:
            form = AddDefaultEmployeeTaskForm(label_suffix='')
            return render(request, 'Process/add_default_task.html', {'form': form, 'return_link': return_link})
    elif action == 'add_default_form_task':
        if request.method == 'POST':
            form = AddDefaultFormBlueprintTaskForm(request.POST)
            if form.is_valid():
                try:
                    default_task = form.cleaned_data['form_bp_name']
                    # request.session['default_tasks'].append(default_task)
                    process_pb.form_bp_defaults.add(default_task)
                    process_pb.save()
                    successfully_added = ' با موفقیت به عنوان پیشنیاز افزوده شد ' + default_task.name + ' وظیفه '
                    return render(request, 'Process/add_default_task.html', {'form': form, 'successfully_added':successfully_added
                                                                             ,'return_link': return_link})
                except ObjectDoesNotExist:
                    message = 'چنین وظیفه‌ای وجود ندارد'
                    return render(request, 'Process/add_default_task.html', {'form': form, 'message': message, 'return_link': return_link})
            else:
                return render(request, 'Process/add_default_task.html', {'form': form, 'return_link': return_link})
        else:
            form = AddDefaultFormBlueprintTaskForm(label_suffix='')
            return render(request, 'Process/add_default_task.html', {'form': form, 'return_link': return_link})
    elif action == 'add_default_payment_task':
        if request.method == 'POST':
            form = AddDefaultPaymentBlueprintTaskForm(request.POST)
            if form.is_valid():
                try:
                    default_task = form.cleaned_data['payment_bp_name']
                    # request.session['default_tasks'].append(default_task)
                    process_pb.payment_bp_defaults.add(default_task)
                    process_pb.save()
                    successfully_added = ' با موفقیت به عنوان پیشنیاز افزوده شد ' + default_task.name + ' وظیفه '
                    return render(request, 'Process/add_default_task.html', {'form': form, 'successfully_added':successfully_added
                                                                             ,'return_link': return_link})
                except ObjectDoesNotExist:
                    message = 'چنین وظیفه‌ای وجود ندارد'
                    return render(request, 'Process/add_default_task.html', {'form': form, 'message': message, 'return_link': return_link})
            else:
                return render(request, 'Process/add_default_task.html', {'form': form, 'return_link': return_link})
        else:
            form = AddDefaultPaymentBlueprintTaskForm(label_suffix='')
            return render(request, 'Process/add_default_task.html', {'form': form, 'return_link': return_link})
    else:
        return render(request, 'Process/process_blueprint_page.html', {'process_pb': process_pb})

def create_employee_task_blueprint(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        return HttpResponseRedirect('/user/login')

    if request.method == 'POST':
        form = CreateEmployeeTaskBlueprintForm(request.POST)
        if form.is_valid():
            employee_task_bp = Employee_Task_Blueprint(name=form.cleaned_data['name'],
                                                       question_set=form.cleaned_data['question_set'])
            employee_task_bp.save()
            return HttpResponseRedirect('/process/create_employee_task_blueprint')
        else:
            return render(request, 'Process/create_employee_task_blueprint.html', {'form': form})
    else:
        form = CreateEmployeeTaskBlueprintForm(label_suffix='')
        return render(request, 'Process/create_employee_task_blueprint.html', {'form': form})



def create_form_blueprint(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        return HttpResponseRedirect('/user/login')

    if request.method == 'POST':
        form = CreateFormBlueprintForm(request.POST)
        if form.is_valid():
            form_bp = Form_Blueprint(name=form.cleaned_data['name'], question_set=Question_Set.objects.get(name=form.cleaned_data['question_set']),
                                     is_timed=form.cleaned_data['is_timed'], max_time=form.cleaned_data['max_time'])
            form_bp.save()
            return HttpResponseRedirect('/process/create_form_blueprint')
        else:
            return render(request, 'Process/create_form_blueprint.html', {'form': form})
    else:
        form = CreateFormBlueprintForm(label_suffix='')
        return render(request, 'Process/create_form_blueprint.html', {'form': form})


def create_payment_blueprint(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        return HttpResponseRedirect('/user/login')

    if request.method == 'POST':
        form = CreatePaymentBlueprintForm(request.POST)
        if form.is_valid():
            payment_bp = Payment_Blueprint(name=form.cleaned_data['name'], receiver=form.cleaned_data['receiver'],
                                           default_amount=form.cleaned_data['default_amount'],
                                           is_timed=form.cleaned_data['is_timed'],
                                           max_time=form.cleaned_data['max_time'])
            #request.session.get('pbps').append(payment_bp)
            payment_bp.save()
            return HttpResponseRedirect('/process/create_payment_blueprint')
        else:
            return render(request, 'Process/create_payment_blueprint.html', {'form': form})
    else:
        form = CreatePaymentBlueprintForm(label_suffix='')
        return render(request, 'Process/create_payment_blueprint.html', {'form': form})



def create_question_set(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        return HttpResponseRedirect('/user/login')
    if request.method == 'POST':
        form = CreateQuestionSetForm(request.POST)
        if form.is_valid():
            question_set = Question_Set(name=form.cleaned_data['name'])
            # if 'question_texts' in request.session.keys():
            #     for i in range(0, len(request.session['question_texts'])):
            #         question = Question(text = request.session['question_texts'][i], type = request.session['question_types'][i],
            #                             belongs_to=question_set)
            #         question.save()
            successfully_added = form.cleaned_data['name']+'با موفقیت ساخته شد'
            question_set.save()
            return render(request, 'Process/create_question_set.html', {'form':form, 'success_message' : successfully_added})
        else:
            return render(request, 'Process/create_question_set.html', {'form': form})
    else:
        form = CreateQuestionSetForm(label_suffix='')
        return render(request, 'Process/create_question_set.html', {'form': form})

def question_set_page(request, name, action=''):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        return HttpResponseRedirect('/user/login')
    try:
        qs = Question_Set.objects.get(name=name)
    except ObjectDoesNotExist:
        return redirect('not_found')
    return_link = '/process/question_set_page/'+name
    if action == 'add_question':
        if request.method == 'POST':
            form = AddQuestionForm(request.POST)
            if form.is_valid():
                question = Question(text = form.cleaned_data['text'], type = form.cleaned_data['type'],
                                    belongs_to=qs)
                # qs.save()
                question.save()
                successfully_added = form.cleaned_data['text']+' با موفقیت اضافه شد '
                return render(request, 'Process/add_question.html', {'form': form,
                                                                     'successfully_added': successfully_added,
                                                                     'return_link': return_link})
            else:
                return render(request, 'Process/add_question.html', {'form': form, 'return_link': return_link})
        else:
            form = AddQuestionForm(label_suffix='')
            return render(request, 'Process/add_question.html', {'form': form, 'return_link': return_link})
    else:
        return render(request, 'Process/question_set_page.html', {'qs': qs})
