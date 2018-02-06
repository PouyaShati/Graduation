from django.shortcuts import render
from Process.models import Process_Blueprint, Employee_Task_Blueprint, Question_Set, Question
from django.http.response import HttpResponseRedirect, HttpResponse
from Process.forms import CreateProcessBlueprintForm, CreateQuestionSetForm, AddQuestionForm, AddPreprocessForm
# Create your views here.


def create_process_blueprint(request, action):
    process_bp = Process_Blueprint()
    if action == 'add_preprocess':
        if request.method == 'POST':
            form = request.POST
            preprocess = form['name']
            process_bp.preprocesses.add(preprocess)

            return HttpResponseRedirect('/process/create_process_blueprint')
        else:
            form = AddPreprocessForm(label_suffix='')
            return render(request, 'Process/create_process_blueprint.html', {'form': form})
    else:
        if request.method == 'POST':
            form = request.POST
            process_bp.name = form['name']
            process_bp.save()
            return HttpResponseRedirect('/')
        else:
            form = CreateProcessBlueprintForm(label_suffix='')
            return render(request, 'Process/create_process_blueprint.html', {'form': form})


def create_question_set(request, action): # TODO handle actions
    question_set = Question_Set()
    if action == 'add_question':
        if request.method == 'POST':
            form = request.POST
            question = Question(text=form['text'], type=form['type'], question_set=question_set)
            question.save()
            return HttpResponseRedirect('/process/create_question_set')
        else:
            form = AddQuestionForm(label_suffix='')
            return render(request, 'Process/create_question_set.html', {'form': form})
    else:
        if request.method == 'POST':
            form = request.POST
            question_set.name = form['name']
            question_set.save()
            return HttpResponseRedirect('/')
        else:
            form = CreateQuestionSetForm(label_suffix='')
            return render(request, 'Process/create_question_set.html', {'form': form})



def create_employee_task_blueprint(request):
    if request.method == 'POST':
        form = request.POST

        employee_task_bp = Employee_Task_Blueprint(name=form['name'], question_set=form['question_set'], default_of=form['default_of']) # TODO get instance of models from form fields
        employee_task_bp.save()

        return HttpResponseRedirect('/process/create_employee_task_blueprint')
    else:
        return render(request, 'Process/create_employee_task_blueprint.html', {'create_employee_task_blueprint_form': CreateEmployeeTaskBlueprintForm(label_suffix='')})
