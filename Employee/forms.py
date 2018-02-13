from django import forms

from .models import Employee, Department
from django.utils.translation import ugettext_lazy as _
from Process.models import Process_Blueprint, Task_Blueprint

class EmployeeSignUpForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^\w+$',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'required': 'True',
                                                              'max_length': 30,
                                                              'placeholder': 'نام کاربری',
                                                              'style': 'text-align:left'}
                                                       ),
                                label=_("نام کاربری"),
                                error_messages={
                                    'invalid': _("تنها استفاده از حروف انگلیسی، اعداد و _ در نام کاربری مجاز است."),
                                    'required': _('لطفا نام کاربری را وارد کنید')})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'required': 'True',
                                                                  'max_length': 30,
                                                                  'render_value': 'False',
                                                                  'placeholder': 'رمز عبور',
                                                                  'style': 'text-align:left'}
                                                           ),
                                label=_("رمز عبور"),
                                error_messages={
                                    'required': _('لطفا رمزعبور را وارد کنید')
                                })
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'required': 'True',
                                                                  'max_length': 30,
                                                                  'render_value': 'False',
                                                                  'placeholder': 'تکرار رمز عبور',
                                                                  'style': 'text-align:left'}
                                                           ),
                                label=_("تکرار رمز عبور"),
                                error_messages={
                                    'required': _('لطفا رمزعبور را تکرار کنید')
                                })

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'employee_id']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'نام',
                                                 'style': 'text-align:right',
                                                 'direction': 'rtl'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'نام خانوادگی',
                                                'style': 'text-align:right',
                                                 'direction': 'rtl'}),
            'email': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'ایمیل',
                                            'style': 'text-align:left'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'شماره تماس',
                                                   'style': 'text-align:left'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'شماره کارمندی',
                                                 'style': 'text-align:left'})
        }
        labels = {
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'email': _('ایمیل'),
            'phone_number': _('شماره تماس'),
            'employee_id': _('شماره کارمندی'),
        }
        error_messages = {
            'first_name': {
                'required': _('لطفا نام را وارد کنید')
            },
            'last_name': {
                'required': _('لطفا نام خانوادگی را وارد کنید')
            },
            'email': {
                'required': _('لطفا ایمیل را وارد کنید'),
                'invalid': _('ایمیل اشتباه است')
            },
            'phone_number': {
                'required': _('لطفا شماره تلفن را وارد کنید'),
                'invalid': _('شماره تلفن اشتباه است')
            },
            'employee_id': {
                'required': _('لطفا شماره کارمندی را وارد کنید'),
                'invalid': _('شماره کارمندی نامعتبر است')
            }
        }

    def clean(self):
        cleaned_data = super(EmployeeSignUpForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('رمزعبور یکسان نیست')
        return cleaned_data




class AddDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'department_id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'نام دپارتمان',
                                                'style': 'text-align:right',
                                                 'direction': 'rtl'}),
            'department_id': forms.NumberInput(attrs={'class': 'form-control',
                                           'placeholder': 'کد دپارتمان',
                                           'style': 'text-align:left'
                                                      })
        }

        labels = {
            'name': _('نام دپارتمان'),
            'department_id': _('کد دپارتمان'),
        }
        error_messages = {
            'name': {
                'required': _('نام دپارتمان را وارد کنید'),
            },
            'department_id': {
                'required': _('شماره دپارتمان را وارد کنید')
            }
        }



class EmployForm(forms.ModelForm):
    # employee_id = forms.RegexField(regex=r'^\d+$',
    #                             widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                           'required': 'True',
    #                                                           'max_length': 30,
    #                                                           'placeholder': 'شماره کارمندی',
    #                                                           'style': 'text-align:right'}
    #                                                    ),
    #                             label=_("شماره کارمندی"),
    #                             error_messages={
    #                                 'invalid': _("تنها استفاده از اعداد در شماره کارمندی مجاز است."),
    #                                 'required': _('لطفا شماره کارمندی را وارد کنید')})
    class Meta:
        model = Employee
        fields = ['employee_id']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'شماره کارمندی',
                                                 'style': 'text-align:left'})
        }
        labels = {
            'employee_id': _('شماره کارمندی')
        }
        error_messages = {
            'employee_id': {
                'invalid': _("تنها استفاده از اعداد در شماره کارمندی مجاز است."),
                'required': _('لطفا شماره کارمندی را وارد کنید')
            }
        }

class FireForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'شماره کارمندی',
                                                 'style': 'text-align:left'})
        }
        labels = {
            'employee_id': _('شماره کارمندی')
        }
        error_messages = {
            'employee_id': {
                'invalid': _("تنها استفاده از اعداد در شماره کارمندی مجاز است."),
                'required': _('لطفا شماره کارمندی را وارد کنید')
            }
        }

class SetManagerForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'شماره کارمندی',
                                                 'style': 'text-align:left'})
        }
        labels = {
            'employee_id': _('شماره کارمندی')
        }
        error_messages = {
            'employee_id': {
                'invalid': _("تنها استفاده از اعداد در شماره کارمندی مجاز است."),
                'required': _('لطفا شماره کارمندی را وارد کنید')
            }
        }

class EmployeePerformTaskForm(forms.Form): # TODO change it in order to be able to retrieve all the answers
    answer = forms.CharField (#regex=r'^\w+$',
                                widget=forms.NumberInput(attrs={'class': 'form-control',
                                                              'required': 'True',
                                                              'max_length': 30,
                                                              #'placeholder': 'preprocess name',
                                                              'style': 'text-align:right',
                                                              'direction': 'rtl'
                                                                }
                                                       ),
                                label=_("paid"),
                                #error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")}
                                )



class AddTaskForm(forms.Form):
    process_bp = forms.ModelChoiceField(queryset=Process_Blueprint.objects.all(),
                                widget=forms.Select(attrs={'class': 'form-control',
                                                              'required': 'True',
                                                              'max_length': 30,
                                                              'placeholder': 'نام فرایند پیشنیاز',
                                                              'style': 'text-align:right',
                                                           'direction': 'rtl'}
                                                       ),
                                label=_("نام فرایند پیشنیاز"),
                                error_messages={
                                    'required': _('نام فرایند پیشنیاز را وارد کنید'),
                                    'invalid': _("نام باید فقط شامل حروف، اعداد و _ باشد")})

    task_bp = forms.ModelChoiceField(queryset=Task_Blueprint.objects.all(),
                                widget=forms.Select(attrs={'class': 'form-control',
                                                              'required': 'True',
                                                              'max_length': 30,
                                                              'placeholder': 'نام الگوی وظیفه',
                                                              'style': 'text-align:right',
                                                           'direction': 'rtl'}
                                                       ),
                                label=_('نام الگوی وظیفه'),
                                error_messages={
                                    'required': _('نام وظیفه را وارد کنید'),
                                    'invalid': _("نام باید فقط شامل حروف، اعداد و _ باشد")})

    student_id = forms.IntegerField (#regex=r'^\w+$',
                                widget=forms.NumberInput(attrs={'class': 'form-control',
                                                              'required': 'True',
                                                              'max_length': 30,
                                                              'placeholder': 'شماره دانشجویی',
                                                              'style': 'text-align:left'
                                                                }
                                                       ),
                                label=_("student_id"),
                                #error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")}
                                )
