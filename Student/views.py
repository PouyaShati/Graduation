from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from MyUser.models import MyUser
from .models import Student
from Student.forms import StudentSignUpForm
# Create your views here.


def student_signup(request):
    if request.method == 'POST':
        form = request.POST
        user = MyUser.objects.create_user(username=form['username'], password=form['password1'], # why "password1" and not just "password" ?
                                        user_type=MyUser.STUDENTUSER)
        user.save()
        student = Student(first_name=form['first_name'], last_name=form['last_name'],
                          email=form['email'], phone_number=form['phone_number'],
                          student_id=form['student_id'], major=form['major']) # Shouldn't we set the value of account_confirmed as well?

        student.user = user
        student.save()
        return HttpResponseRedirect('/student/student_login')
    else:
        return render(request, 'Student/student_signup.html', {'signup_form': StudentSignUpForm(label_suffix='')})