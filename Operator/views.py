from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from MyUser.models import MyUser
from django.contrib.auth import authenticate, login, logout
from .forms import OperatorSignUpForm
from .models import Operator
# Create your views here.


def operator_signup(request):
    if request.method == 'POST':
        form = OperatorSignUpForm(request.POST)
        if form.is_valid():
            user = MyUser.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'],
                                              user_type=MyUser.ADMINUSER)
            user.save()
            operator = Operator(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                              email=form.cleaned_data['email'], phone_number=form.cleaned_data['phone_number'])

            operator.user = user

            operator.save()

            return HttpResponseRedirect('/operator/login')
        else:

            return render(request, 'Operator/operator_signup.html', {'signup_form': form})
    else:
        return render(request, 'Operator/operator_signup.html', {'signup_form': OperatorSignUpForm(label_suffix='')})


def operator_login(request):
    if request.method == 'GET':
        return render(request, 'Operator/operator_login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if (user is not None) and (user.user_type == MyUser.ADMINUSER):
            login(request, user)
            return HttpResponseRedirect('/operator/panel')
        else:
            message = 'نام کاربری یا رمز عبور اشتباه است'
            return render(request, 'Operator/operator_login.html', {'message': message},status=403)


def operator_logout(request):
    logout(request)
    return HttpResponseRedirect('/operator/login')


def operator_panel(request): #, action):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/operator/login')
    if request.user.user_type != MyUser.ADMINUSER:
        return HttpResponseRedirect('/operator/login')

    return render(request, 'Operator/operator_panel.html',
                  {'operator': request.user.Operator})