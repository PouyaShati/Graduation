from django import forms

from .models import Student
from django.utils.translation import ugettext_lazy as _


class StudentSignUpForm(forms.ModelForm):
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
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'student_id', 'major', 'document']
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
            'student_id': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'شماره دانشجویی',
                                                 'style': 'text-align:left'}),
            'major': forms.Select(choices=Student.majors, attrs={'class': 'form-control'})
                                                                 #'style': 'text-align:right'
        }
        labels = {
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'email': _('ایمیل'),
            'phone_number': _('شماره تماس'),
            'student_id': _('شماره دانشجویی'),
            'major': _('رشته تحصیلی'),
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
            'student_id': {
                'required': _('لطفا شماره دانشجویی را وارد کنید'),
                'invalid': _('شماره دانشجویی نامعتبر است')
            },
            'major': {
                'required': _('لطفا رشته تحصیلی را انتخاب کنید')
            }
        }

    def clean(self):
        cleaned_data = super(StudentSignUpForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('رمزعبور یکسان نیست')
        return cleaned_data


class StudentPerformPaymentForm(forms.ModelForm):
    paid = forms.IntegerField (#regex=r'^\w+$',
                                widget=forms.NumberInput(attrs={'class': 'form-control',
                                                              'required': 'True',
                                                              'max_length': 30,
                                                              'placeholder': 'میزان پرداختی',
                                                              'style': 'text-align:left'
                                                                }
                                                       ),
                                label=_("paid"),
                                #error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")}
                                )


class StudentFillFormForm(forms.ModelForm): # TODO change it in order to be able to retrieve all the answers
    answer = forms.CharField (#regex=r'^\w+$',
                                widget=forms.NumberInput(attrs={'class': 'form-control',
                                                              'required': 'True',
                                                              'max_length': 30,
                                                              'placeholder': 'پاسخ به سوال',
                                                                'style': 'text-align:right',
                                                                'direction': 'rtl'
                                                                }
                                                       ),
                                label=_("answer"),
                                #error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")}
                                )