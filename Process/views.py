from django.shortcuts import render
from Process.models import Process_Blueprint, Employee_Task_Blueprint, Question_Set, Question, Form_Blueprint, Payment_Blueprint
from django.http.response import HttpResponseRedirect, HttpResponse
from Process.forms import CreateProcessBlueprintForm, CreateQuestionSetForm, AddQuestionForm, AddPreprocessForm, CreateEmployeeTaskBlueprintForm
from Process.forms import CreateFormBlueprintForm, CreatePaymentBlueprintForm
# Create your views here.


def create_process_blueprint(request, action): # TODO handle actions
    if action == 'add_preprocess':
        if request.method == 'POST':
            form = request.POST
            preprocess = Process_Blueprint.objects.get(name=form['name'])
            request.session['preprocesses'].append(preprocess)
            #process_bp.preprocesses.add(preprocess)
            return HttpResponseRedirect('/process/create_process_blueprint')
        else:
            form = AddPreprocessForm(label_suffix='')
            return render(request, 'Process/add_preprocess.html', {'form': form})
    elif action == 'create_employee_task_blueprint':
        if request.method == 'POST':
            form = request.POST
            employee_task_bp = Employee_Task_Blueprint(name=form['name'], question_set=request.session.get('questions'))
            request.session.get('etbs').append(employee_task_bp)
            employee_task_bp.save()
            return HttpResponseRedirect('/process/create_process_blueprint')
        else:
            return render(request, 'Process/create_employee_task_blueprint.html', {'create_employee_task_blueprint_form': CreateEmployeeTaskBlueprintForm(label_suffix='')})
    elif action == 'create_form_blueprint':
        if request.method == 'POST':
            form = request.POST
            form_bp = Form_Blueprint(name=form['name'], question_set=request.session.get('questions'),
                                     is_timed=form['is_timed'], max_time=form['max_time'])
            request.session.get('fbps').append(form_bp)
            form_bp.save()
            return HttpResponseRedirect('/process/create_process_blueprint')
        else:
            return render(request, 'Process/create_form_blueprint.html', {'create_form_blueprint_form': CreateFormBlueprintForm(label_suffix='')})
    elif action == 'create_payment_blueprint':
        if request.method == 'POST':
            form = request.POST
            payment_bp = Payment_Blueprint(name=form['name'], receiver=form['receiver'], default_amount=form['default_amount'],
                                     is_timed=form['is_timed'], max_time=form['max_time'])
            request.session.get('pbps').append(payment_bp)
            payment_bp.save()
            return HttpResponseRedirect('/process/create_process_blueprint')
        else:
            return render(request, 'Process/create_payment_blueprint.html', {'create_payment_blueprint_form': CreatePaymentBlueprintForm(label_suffix='')})

    elif action == 'create_question_set':
        if request.method == 'POST':
            form = request.POST
            question_set = Question_Set(name=form['name'])
            for q in request.session.get('questions'):
                q.belongs_to = question_set
            question_set.save()
            request.session['question_set'] = question_set
            return HttpResponseRedirect('/process/create_process_blueprint')
        else:
            request.session['questions'] = []
            form = CreateQuestionSetForm(label_suffix='')
            return render(request, 'Process/create_question_set.html', {'form': form})

    elif action == 'add_question':
        if request.method == 'POST':
            form = request.POST
            question = Question(text=form['text'], type=form['type'])
            request.session.get('questions').append(question)
            question.save()
            return HttpResponseRedirect('/process/create_process_blueprint')
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
            # form = CreateProcessBlueprintForm(request.POST)
            form = request.POST
            process_bp = Process_Blueprint(name=form['name'])
            for preprocess in request.session.get('preprocesses'):
                process_bp.preprocesses.add(preprocess)
            process_bp.save()
            return HttpResponseRedirect('/')