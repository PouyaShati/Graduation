from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def slash(request):
    return redirect('/homepage/')

def homepage(request):
    return render(request, 'homepage/homepage.html')

def handle404(request):
    return render(request, 'homepage/404.html')