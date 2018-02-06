from django.shortcuts import render
from Process.models import Process_Blueprint, Employee_Task_Blueprint, Question_Set
from django.http.response import HttpResponseRedirect, HttpResponse
from Process.forms import CreateProcessBlueprintForm
# Create your views here.


def create_process_blueprint(request):
    return HttpResponse('Hello Sadra')
    '''
    if request.method == 'POST':
        form = request.POST

        process_bp = Process_Blueprint(name=form['name'])
        process_bp.save()

        for preprocess_bp in Process_Blueprint.objects.all():
            if form['preprocess_' + preprocess_bp.name]:
                process_bp.preprocesses.add(preprocess_bp)


        return HttpResponseRedirect('/process/create_process_blueprint')
    else:
        return render(request, 'Process/create_process_blueprint.html', {'create_process_blueprint_form': CreateProcessBlueprintForm(label_suffix='')})
    '''
'''
def create_question_set(request):
    if request.method == 'POST':
        form = request.POST

        question_set = Question_Set(name=form['name'])

        # TODO add all the questions retrieved form form to question_set


        return HttpResponseRedirect('/process/create_question_set')
    else:
        return render(request, 'Process/create_question_set.html', {'create_question_set_form': CreateQuestionSetForm(label_suffix='')})
'''

'''
def create_employee_task_blueprint(request):
    if request.method == 'POST':
        form = request.POST

        employee_task = Employee_Task_Blueprint(name=form['name'])
        process_bp.save()

        for preprocess in form['preprocesses']:
            process_bp.preprocesses.add(Process_Blueprint.objects.get(name=preprocess)) # handle the error when there's not a blueprint with preprocess as its name


        return HttpResponseRedirect('/process/create_process_blueprint')
    else:
        return render(request, 'Process/create_process_blueprint.html', {'create_process_blueprint_form': CreateProcessBlueprintForm(label_suffix='')})
'''
