from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from MyUser.models import MyUser
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def user_login(request):
    if request.method == 'GET':
        return render(request, 'MyUser/login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == MyUser.STUDENTUSER:
                return HttpResponseRedirect('/student/panel')
            elif user.user_type == MyUser.EMPLOYEEUSER:
                return HttpResponseRedirect('/employee/panel')
            elif user.user_type == MyUser.ADMINUSER:
                return HttpResponseRedirect('/operator/panel')
        else:
            message = 'نام کاربری یا رمز عبور اشتباه است'
            return render(request, 'MyUser/login.html', {'message': message},status=403)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/user/login')
