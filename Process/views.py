from django.shortcuts import render
from Process.models import Process_Blueprint
from django.http.response import HttpResponseRedirect
from Process.forms import CreateProcessBlueprint
# Create your views here.


def create_process_blueprint(request):
    if request.method == 'POST':
        form = request.POST

        process_bp = Process_Blueprint(name=form['name'])
        process_bp.save()

        for preprocess in form['preprocesses']:
            process_bp.preprocesses.add(Process_Blueprint.objects.get(name=preprocess)) # handle the error when there's not a blueprint with preprocess as its name


        return HttpResponseRedirect('/process/create_process_blueprint')
    else:
        return render(request, 'Process/create_process_blueprint.html', {'create_process_blueprint_form': CreateProcessBlueprintForm(label_suffix='')})


