from django.shortcuts import render
from Process.models import Process_Blueprint, Employee_Task_Blueprint, Question_Set, Question, Form_Blueprint, Payment_Blueprint
from Employee.models import Department, Employee
from django.http.response import HttpResponseRedirect, HttpResponse
from Process.forms import CreateProcessBlueprintForm, CreateQuestionSetForm, AddQuestionForm, AddPreprocessForm, CreateEmployeeTaskBlueprintForm
from Process.forms import CreateFormBlueprintForm, CreatePaymentBlueprintForm
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def create_process_blueprint(request, action): # TODO handle actions

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/Employee/employee_login')
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        return HttpResponseRedirect('/Employee/employee_login')

    employee = Employee.objects.get(user= request.user)
    department = Department.objects.get(manager= employee)
    if department == None:
        return HttpResponseRedirect('/Employee/employee_login')

    if action == 'add_preprocess':
        if request.method == 'POST':
            form = AddPreprocessForm(request.POST)
            if form.is_valid():
                try:
                    # request.session['preprocesses'] = []

                    # n = int(form_set['form-TOTAL_FORMS'])
                    # for i in range(0, n):
                    #     request.session['preprocesses'].append(form_set['form-' + str(i) + '-name'])

                        new_preprocess = form.cleaned_data['name']
                        request.session['preprocesses'].append(new_preprocess)

                        # ret   urn HttpResponseRedirect('/process/create_process_blueprint')
                        successfully_added = ' با موفقیت به عنوان پیشنیاز افزوده شد ' + new_preprocess.name+ ' فرایند '
                        return render(request, 'Process/add_preprocess.html', {'form': form, 'successfully_added':successfully_added})
                except ObjectDoesNotExist:
                    message = 'چنین فرایندی وجود ندارد'
                    return render(request, 'Process/add_preprocess.html', {'form': form, 'message': message})
            else:
                return render(request, 'Process/add_preprocess.html', {'form': form})
        else:
            form = AddPreprocessForm(label_suffix='')
            request.session['preprocesses'] = []
            return render(request, 'Process/add_preprocess.html', {'form': form})
    else:
        if request.method == 'GET':

            form = CreateProcessBlueprintForm(label_suffix='')
            return render(request, 'Process/create_process_blueprint.html', {'form': form})
        else:
            form = CreateProcessBlueprintForm(request.POST)
            if form.is_valid():
                try:
                    #department = form.cleaned_data['department']
                    process_bp = Process_Blueprint(name=form.cleaned_data['name'], department=department)
                    if 'preprocesses' in request.session.keys():
                        for preprocess_name in request.session['preprocesses']:
                            preprocess = Process_Blueprint.objects.get(name=preprocess_name)
                            process_bp.preprocesses.add(preprocess)
                            del request.session['preprocesses']
                    process_bp.save()

                    return HttpResponseRedirect('/')
                except ObjectDoesNotExist:
                    return render(request, 'Process/create_process_blueprint.html', {'form': form})
            else:
                return render(request, 'Process/create_process_blueprint.html', {'form': form})



def create_employee_task_blueprint(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/Employee/employee_login')
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        return HttpResponseRedirect('/Employee/employee_login')

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
        return HttpResponseRedirect('/Employee/employee_login')
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        return HttpResponseRedirect('/Employee/employee_login')

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
        return HttpResponseRedirect('/Employee/employee_login')
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        return HttpResponseRedirect('/Employee/employee_login')

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



def create_question_set(request, action):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/Employee/employee_login')
    if request.user.user_type != MyUser.EMPLOYEEUSER:
        return HttpResponseRedirect('/Employee/employee_login')

    if action == 'set_questions':
        if request.method == 'POST':
            form = AddQuestionForm(request.POST)
            if form.is_valid():
                # question_set = Question_Set(name=form.cleaned_data['name'])
                # for q in request.session.get('questions'):
                #    q.belongs_to = question_set

                # request.session['question_texts'] = []
                # request.session['question_types'] = []
                #
                # n = int(form_set['form-TOTAL_FORMS'])
                # for i in range(0, n):
                #     request.session['question_texts'].append(form_set['form-' + str(i) + '-text'])
                #     request.session['question_types'].append(form_set['form-' + str(i) + '-type'])
                new_question_text = form.cleaned_data['text']
                new_question_tpye = form.cleaned_data['type']
                request.session['question_texts'].append(new_question_text)
                request.session['question_types'].append(new_question_tpye)
                successfully_added = new_question_text + 'با موفقیت اضافه شد'
                # return HttpResponseRedirect('/process/create_question_set')
                return render(request, 'Process/set_questions.html', {'form': form, 'successfully_added':successfully_added})
            else:
                return render(request, 'Process/set_questions.html', {'form': form})
        else:
            request.session['question_texts'] = []
            request.session['question_types'] = []
            form = AddQuestionForm(label_suffix='')
            return render(request, 'Process/set_questions.html', {'form': form})
    else:
        if request.method == 'POST':
            form = CreateQuestionSetForm(request.POST)
            if form.is_valid():
                question_set = Question_Set(name=form['name'])
                if 'question_texts' in request.session.keys():
                    for i in range(0, len(request.session['question_texts'])):
                        question = Question(text = request.session['question_texts'][i], type = request.session['question_types'][i],
                                            belongs_to=question_set)
                        question.save()

                question_set.save()
                return HttpResponseRedirect('/process/create_question_set')
            else:
                return render(request, 'Process/create_question_set.html', {'form': form})
        else:
            form = CreateQuestionSetForm(label_suffix='')
            return render(request, 'Process/create_question_set.html', {'form': form})