from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from MyUser.models import MyUser
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def admin_signup(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            user = MyUser.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'],
                                              user_type=MyUser.ADMINUSER)
            user.save()
            admin = Admin(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                              email=form.cleaned_data['email'], phone_number=form.cleaned_data['phone_number'])

            admin.user = user

            admin.save()

            return HttpResponseRedirect('/admin/login')
        else:

            return render(request, 'Admin/admin_signup.html', {'signup_form': form})
    else:
        return render(request, 'Admin/admin_signup.html', {'signup_form': AdminSignUpForm(label_suffix='')})


def admin_login(request):
    if request.method == 'GET':
        return render(request, 'Admin/admin_login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if (user is not None) and (user.user_type == MyUser.ADMINUSER):
            login(request, user)
            return HttpResponseRedirect('/admin/panel')
        else:
            message = 'نام کاربری یا رمز عبور اشتباه است'
            return render(request, 'Admin/admin_login.html', {'message': message},status=403)


def admin_logout(request):
    logout(request)
    return HttpResponseRedirect('/admin/login')


def admin_panel(request): #, action):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/admin/login')
    if request.user.user_type != MyUser.ADMINUSER:
        return HttpResponseRedirect('/admin/login')

    return render(request, 'Admin/admin_panel.html',
                  {'admin': request.user.Admin})