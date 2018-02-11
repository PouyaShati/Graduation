from django.shortcuts import render, redirect, reverse
from Process.models import Process_Blueprint, Employee_Task_Blueprint, Question_Set, Question, Form_Blueprint, Payment_Blueprint, Task_Blueprint
from Employee.models import Department, Employee
from django.http.response import HttpResponseRedirect, HttpResponse
from Process.forms import CreateProcessBlueprintForm, CreateQuestionSetForm, AddQuestionForm, AddPreprocessForm, CreateEmployeeTaskBlueprintForm
from Process.forms import CreateFormBlueprintForm, CreatePaymentBlueprintForm, AddDefaultEmployeeTaskForm, AddDefaultFormBlueprintTaskForm, AddDefaultPaymentBlueprintTaskForm
from Process.forms import CreateProcessBlueprintOperatorForm
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from MyUser.models import MyUser
# Create your views here.


def create_process_blueprint(request): # TODO handle actions

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.EMPLOYEEUSER and request.user.user_type != MyUser.ADMINUSER:
        return HttpResponseRedirect('/user/login')



    if request.user.user_type == MyUser.EMPLOYEEUSER:
        base_html = 'base/emp_base.html'
        created = False
        employee = Employee.objects.get(user= request.user)
        try:
            department = Department.objects.get(manager= employee)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/user/login')
        if department is None:
            return HttpResponseRedirect('/employee/login')

        if request.method == 'GET':
            form = CreateProcessBlueprintForm(label_suffix='')
            return render(request, 'Process/create_process_blueprint.html', {'form': form, 'base_html':base_html})
        else:
            form = CreateProcessBlueprintForm(request.POST)
            if form.is_valid():
                try:
                    process_bp = Process_Blueprint(name=form.cleaned_data['name'], department=department)

                    process_bp.save()
                    success_message = ' با موفقیت ساخته شد '+form.cleaned_data['name']
                    name = form.cleaned_data['name']
                    return render(request, 'Process/create_process_blueprint.html', {'form': form, 'success_message':success_message
                                                                                     , 'base_html': base_html, 'name': name})
                except ObjectDoesNotExist:
                    return render(request, 'Process/create_process_blueprint.html', {'form': form})
            else:
                return render(request, 'Process/create_process_blueprint.html', {'form': form, 'base_html': base_html})
    else:
        base_html = 'base/op_base.html'
        if request.method == 'GET':
            form = CreateProcessBlueprintOperatorForm(label_suffix='')
            return render(request, 'Process/create_process_blueprint.html', {'form': form, 'base_html': base_html})
        else:
            form = CreateProcessBlueprintOperatorForm(request.POST)
            if form.is_valid():
                process_bp = Process_Blueprint(name=form.cleaned_data['name'], department=form.cleaned_data['department'])
                process_bp.save()
                success_message = ' با موفقیت ساخته شد '+form.cleaned_data['name']
                name = form.cleaned_data['name']
                return render(request, 'Process/create_process_blueprint.html', {'form': form, 'success_message': success_message
                                                                                 , 'base_html': base_html, 'name': name})
            else:
                return render(request, 'Process/create_process_blueprint.html', {'form': form, 'base_html': base_html})



def process_blueprint_page(request, name, action=''):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.EMPLOYEEUSER and request.user.user_type != MyUser.ADMINUSER:
        return HttpResponseRedirect('/user/login')
    if request.user.user_type == MyUser.ADMINUSER:
        base_html = 'base/op_base.html'
    else:
        base_html = 'base/emp_base.html'
    # employee = Employee.objects.get(user= request.user)
    # try:
    #     department = Department.objects.get(manager= employee)
    # except ObjectDoesNotExist:
    #     return HttpResponseRedirect('/user/login')
    # if department is None:
    #     return HttpResponseRedirect('/employee/login')
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
                                                                               'return_link': return_link, 'base_html': base_html})
                        # return render(request, 'Process/create_process_blueprint.html', {'form': CreateProcessBlueprintForm(label_suffix='')})
                except ObjectDoesNotExist:
                    message = 'چنین فرایندی وجود ندارد'
                    return render(request, 'Process/add_preprocess.html', {'form': form, 'message': message, 'return_link': return_link
                                                                           , 'base_html': base_html})
            else:
                return render(request, 'Process/add_preprocess.html', {'form': form, 'return_link': return_link, 'base_html': base_html})
        else:
            form = AddPreprocessForm(label_suffix='')
            return render(request, 'Process/add_preprocess.html', {'form': form, 'return_link': return_link, 'base_html': base_html})
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
                                                                             ,'return_link': return_link, 'base_html': base_html})
                except ObjectDoesNotExist:
                    message = 'چنین وظیفه‌ای وجود ندارد'
                    return render(request, 'Process/add_default_task.html', {'form': form, 'message': message, 'return_link': return_link, 'base_html': base_html})
            else:
                return render(request, 'Process/add_default_task.html', {'form': form, 'return_link': return_link, 'base_html': base_html})
        else:
            form = AddDefaultEmployeeTaskForm(label_suffix='')
            return render(request, 'Process/add_default_task.html', {'form': form, 'return_link': return_link, 'base_html': base_html})
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
                                                                             ,'return_link': return_link, 'base_html': base_html})
                except ObjectDoesNotExist:
                    message = 'چنین وظیفه‌ای وجود ندارد'
                    return render(request, 'Process/add_default_task.html', {'form': form, 'message': message, 'return_link': return_link, 'base_html': base_html})
            else:
                return render(request, 'Process/add_default_task.html', {'form': form, 'return_link': return_link, 'base_html': base_html})
        else:
            form = AddDefaultFormBlueprintTaskForm(label_suffix='')
            return render(request, 'Process/add_default_task.html', {'form': form, 'return_link': return_link, 'base_html': base_html})
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
                                                                             ,'return_link': return_link, 'base_html': base_html})
                except ObjectDoesNotExist:
                    message = 'چنین وظیفه‌ای وجود ندارد'
                    return render(request, 'Process/add_default_task.html', {'form': form, 'message': message, 'return_link': return_link, 'base_html': base_html})
            else:
                return render(request, 'Process/add_default_task.html', {'form': form, 'return_link': return_link, 'base_html': base_html})
        else:
            form = AddDefaultPaymentBlueprintTaskForm(label_suffix='')
            return render(request, 'Process/add_default_task.html', {'form': form, 'return_link': return_link, 'base_html': base_html})
    else:
        return render(request, 'Process/process_blueprint_page.html', {'process_pb': process_pb, 'base_html': base_html})

def create_employee_task_blueprint(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.EMPLOYEEUSER and request.user.user_type != MyUser.ADMINUSER:
        return HttpResponseRedirect('/user/login')
    if request.user.user_type == MyUser.ADMINUSER:
        base_html = 'base/op_base.html'
    else:
        base_html = 'base/emp_base.html'

    if request.method == 'POST':
        form = CreateEmployeeTaskBlueprintForm(request.POST)
        if form.is_valid():
            employee_task_bp = Employee_Task_Blueprint(name=form.cleaned_data['name'],
                                                       question_set=form.cleaned_data['question_set'])
            employee_task_bp.save()
            success = ' با موفقیت اضافه شد '+ form.cleaned_data['name']
            return render(request, 'Process/create_employee_task_blueprint.html', {'form': form, 'base_html': base_html
                                                                                   , 'success': success})
        else:
            return render(request, 'Process/create_employee_task_blueprint.html', {'form': form, 'base_html': base_html})
    else:
        form = CreateEmployeeTaskBlueprintForm(label_suffix='')
        return render(request, 'Process/create_employee_task_blueprint.html', {'form': form, 'base_html': base_html})



def create_form_blueprint(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.EMPLOYEEUSER and request.user.user_type != MyUser.ADMINUSER:
        return HttpResponseRedirect('/user/login')
    if request.user.user_type == MyUser.ADMINUSER:
        base_html = 'base/op_base.html'
    else:
        base_html = 'base/emp_base.html'


    if request.method == 'POST':
        form = CreateFormBlueprintForm(request.POST)
        if form.is_valid():
            form_bp = Form_Blueprint(name=form.cleaned_data['name'], question_set=Question_Set.objects.get(name=form.cleaned_data['question_set']),
                                     is_timed=form.cleaned_data['is_timed'], max_time=form.cleaned_data['max_time'])
            form_bp.save()
            success = ' با موفقیت اضافه شد '+form.cleaned_data['name']
            return render(request, 'Process/create_form_blueprint.html', {'form': form, 'base_html': base_html, 'success': success})
        else:
            return render(request, 'Process/create_form_blueprint.html', {'form': form, 'base_html': base_html})
    else:
        form = CreateFormBlueprintForm(label_suffix='')
        return render(request, 'Process/create_form_blueprint.html', {'form': form, 'base_html': base_html})


def create_payment_blueprint(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.EMPLOYEEUSER and request.user.user_type != MyUser.ADMINUSER:
        return HttpResponseRedirect('/user/login')
    if request.user.user_type == MyUser.ADMINUSER:
        base_html = 'base/op_base.html'
    else:
        base_html = 'base/emp_base.html'


    if request.method == 'POST':
        form = CreatePaymentBlueprintForm(request.POST)
        if form.is_valid():
            payment_bp = Payment_Blueprint(name=form.cleaned_data['name'], receiver=form.cleaned_data['receiver'],
                                           default_amount=form.cleaned_data['default_amount'],
                                           is_timed=form.cleaned_data['is_timed'],
                                           max_time=form.cleaned_data['max_time'])
            #request.session.get('pbps').append(payment_bp)
            payment_bp.save()
            success = ' با موفقیت اضافه شد '+form.cleaned_data['name']
            return render(request, 'Process/create_payment_blueprint.html', {'form': form, 'base_html': base_html,
                                                                              'success':success})
        else:
            return render(request, 'Process/create_payment_blueprint.html', {'form': form, 'base_html':base_html})
    else:
        form = CreatePaymentBlueprintForm(label_suffix='')
        return render(request, 'Process/create_payment_blueprint.html', {'form': form, 'base_html': base_html})



def create_question_set(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.EMPLOYEEUSER and request.user.user_type != MyUser.ADMINUSER:
        return HttpResponseRedirect('/user/login')
    if request.user.user_type == MyUser.ADMINUSER:
        base_html = 'base/op_base.html'
    else:
        base_html = 'base/emp_base.html'

    if request.method == 'POST':
        form = CreateQuestionSetForm(request.POST)
        if form.is_valid():
            question_set = Question_Set(name=form.cleaned_data['name'])
            # if 'question_texts' in request.session.keys():
            #     for i in range(0, len(request.session['question_texts'])):
            #         question = Question(text = request.session['question_texts'][i], type = request.session['question_types'][i],
            #                             belongs_to=question_set)
            #         question.save()
            successfully_added = 'با موفقیت ساخته شد '+form.cleaned_data['name']
            question_set.save()
            name = form.cleaned_data['name']
            return render(request, 'Process/create_question_set.html', {'form':form, 'success_message' : successfully_added,
                                                                        'base_html': base_html,'name': name})
        else:
            return render(request, 'Process/create_question_set.html', {'form': form, 'base_html': base_html})
    else:
        form = CreateQuestionSetForm(label_suffix='')
        return render(request, 'Process/create_question_set.html', {'form': form, 'base_html': base_html})

def question_set_page(request, name, action=''):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login')
    if request.user.user_type != MyUser.EMPLOYEEUSER and request.user.user_type != MyUser.ADMINUSER:
        return HttpResponseRedirect('/user/login')
    if request.user.user_type == MyUser.ADMINUSER:
        base_html = 'base/op_base.html'
    else:
        base_html = 'base/emp_base.html'
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
                successfully_added = ' با موفقیت اضافه شد '+form.cleaned_data['text']
                return render(request, 'Process/add_question.html', {'form': form,
                                                                     'successfully_added': successfully_added,
                                                                     'return_link': return_link, 'base_html': base_html
                                                                     })
            else:
                return render(request, 'Process/add_question.html', {'form': form, 'return_link': return_link, 'base_html': base_html})
        else:
            form = AddQuestionForm(label_suffix='')
            return render(request, 'Process/add_question.html', {'form': form, 'return_link': return_link, 'base_html': base_html})
    else:
        return render(request, 'Process/question_set_page.html', {'qs': qs, 'base_html': base_html})
