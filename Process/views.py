from django.shortcuts import render
from Process.models import Process_Blueprint, Employee_Task_Blueprint, Question_Set, Question, Form_Blueprint, Payment_Blueprint
from Employee.models import Department
from django.http.response import HttpResponseRedirect, HttpResponse
from Process.forms import CreateProcessBlueprintForm, CreateQuestionSetForm, AddQuestionForm, AddPreprocessForm, CreateEmployeeTaskBlueprintForm
from Process.forms import CreateFormBlueprintForm, CreatePaymentBlueprintForm
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def create_process_blueprint(request, action): # TODO handle actions
    if action == 'add_preprocess':
        if request.method == 'POST':
            form = AddPreprocessForm(request.POST)
            if form.is_valid():
                try:
                    preprocess = Process_Blueprint.objects.get(name=form.cleaned_data['name'])
                    request.session['preprocesses'].append(preprocess)
                    #process_bp.preprocesses.add(preprocess)
                    return HttpResponseRedirect('/process/create_process_blueprint')
                except ObjectDoesNotExist:
                    message = 'چنین فرایندی وجود ندارد'
                    return render(request, 'Process/add_preprocess.html', {'form': form, 'message':message})
            else:
                return render(request, 'Process/add_preprocess.html', {'form': form})
        else:
            form = AddPreprocessForm(label_suffix='')
            return render(request, 'Process/add_preprocess.html', {'form': form})
    elif action == 'create_employee_task_blueprint':
        if request.method == 'POST':
            form = CreateEmployeeTaskBlueprintForm(request.POST)
            if form.is_valid():
                employee_task_bp = Employee_Task_Blueprint(name=form.cleaned_data['name'], question_set=request.session.get('questions'))
                request.session.get('etbs').append(employee_task_bp)
                employee_task_bp.save()
                return HttpResponseRedirect('/process/create_process_blueprint')
            else:
                return render(request, 'Process/create_employee_task_blueprint.html', {'form': form})
        else:
            form = CreateEmployeeTaskBlueprintForm(label_suffix='')
            return render(request, 'Process/create_employee_task_blueprint.html', {'form': form})
    elif action == 'create_form_blueprint':
        if request.method == 'POST':
            form = CreateFormBlueprintForm(request.POST)
            if form.is_valid():
                form_bp = Form_Blueprint(name=form.cleaned_data['name'], question_set=request.session.get('questions'),
                                         is_timed=form.cleaned_data['is_timed'], max_time=form.cleaned_data['max_time'])
                request.session.get('fbps').append(form_bp)
                form_bp.save()
                return HttpResponseRedirect('/process/create_process_blueprint')
            else:
                return render(request, 'Process/create_form_blueprint.html', {'form': form})
        else:
            form = CreateFormBlueprintForm(label_suffix='')
            return render(request, 'Process/create_form_blueprint.html', {'form': form})
    elif action == 'create_payment_blueprint':
        if request.method == 'POST':
            form = CreatePaymentBlueprintForm(request.POST)
            if form.is_valid():
                payment_bp = Payment_Blueprint(name=form.cleaned_data['name'], receiver=form.cleaned_data['receiver'], default_amount=form.cleaned_data['default_amount'],
                                         is_timed=form.cleaned_data['is_timed'], max_time=form.cleaned_data['max_time'])
                request.session.get('pbps').append(payment_bp)
                payment_bp.save()
                return HttpResponseRedirect('/process/create_process_blueprint')
            else:
                return render(request, 'Process/create_payment_blueprint.html', {'form': form})
        else:
            form = CreateFormBlueprintForm(label_suffix='')
            return render(request, 'Process/create_payment_blueprint.html', {'form': form})

    elif action == 'create_question_set':
        if request.method == 'POST':
            form = CreateQuestionSetForm(request.POST)
            if form.is_valid():
                question_set = Question_Set(name=form.cleaned_data['name'])
                for q in request.session.get('questions'):
                    q.belongs_to = question_set
                question_set.save()
                request.session['question_set'] = question_set
                return HttpResponseRedirect('/process/create_process_blueprint')
            else:
                return render(request, 'Process/create_question_set.html', {'form': form})
        else:
            request.session['questions'] = []
            form = CreateQuestionSetForm(label_suffix='')
            return render(request, 'Process/create_question_set.html', {'form': form})

    elif action == 'add_question':
        if request.method == 'POST':
            form = AddQuestionForm(request.POST)
            if form.is_valid():
                question = Question(text=form.cleaned_data['text'], type=form.cleaned_data['type'])
                request.session.get('questions').append(question)
                question.save()
                return HttpResponseRedirect('/process/create_process_blueprint')
            else:
                return render(request, 'Process/add_question.html', {'form': form})
        else:
            form = AddQuestionForm(label_suffix='')
            return render(request, 'Process/add_question.html', {'form': form})
    else:
        if request.method == 'GET':
            request.session['preprocesses'] = []
            request.session['etbs'] = []
            request.session['fbps'] = []
            request.session['pbps'] = []
            form = CreateProcessBlueprintForm(label_suffix='')
            return render(request, 'Process/create_process_blueprint.html', {'form': form})
        else:
            form = CreateProcessBlueprintForm(request.POST)
            if form.is_valid():
                try:
                    department = Department.objects.get(name=form.cleaned_data['department'])
                    process_bp = Process_Blueprint(name=form.cleaned_data['name'], department=department)
                    for preprocess in request.session.get('preprocesses'):
                        process_bp.preprocesses.add(preprocess)
                    process_bp.save()
                    return HttpResponseRedirect('/')
                except ObjectDoesNotExist:
                    return render(request, 'Process/create_process_blueprint.html', {'form': form})
            else:
                return render(request, 'Process/create_process_blueprint.html', {'form': form})
