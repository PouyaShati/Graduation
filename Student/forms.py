from django import forms

from .models import Student
from django.utils.translation import ugettext_lazy as _
#from Administrator.models import ProviderProvideRequest


class StudentSignUpForm(forms.ModelForm):

    username = forms.RegexField(regex=r'^\w+$',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'required': 'True',
                                                              'max_length': 30,
                                                              'placeholder': 'نام کاربری',
                                                              'style': 'text-align:right'}
                                                       ),
                                label=_("نام کاربری"),
                                error_messages={
                                    'invalid': _("تنها استفاده از حروف انگلیسی، اعداد و _ در نام کاربری مجاز است.")})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'required': 'True',
                                                                  'max_length': 30,
                                                                  'render_value': 'False',
                                                                  'placeholder': 'رمز عبور',
                                                                  'style': 'text-align:right'}
                                                           ),
                                label=_("رمز عبور"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'required': 'True',
                                                                  'max_length': 30,
                                                                  'render_value': 'False',
                                                                  'placeholder': 'تکرار رمز عبور',
                                                                  'style': 'text-align:right'}
                                                           ),
                                label=_("تکرار رمز عبور"))

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'student_id', 'major']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'نام',
                                           'style': 'text-align:right'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': 'نام خانوادگی',
                                                       'style': 'text-align:right'}),
            'email': forms.TextInput(attrs={'class': 'form-control',
                                                      'placeholder': 'ایمیل',
                                                      'style': 'text-align:left'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'شماره تماس',
                                            'style': 'text-align:left'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'شماره دانشجویی',
                                                   'style': 'text-align:left'}),
            'major': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'رشته تحصیلی',
                                              'style': 'text-align:right'}),

        }
        labels = {
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'email': _('ایمیل'),
            'phone_number': _('شماره تماس'),
            'student_id': _('شماره دانشجویی'),
            'major': _('رشته تحصیلی'),
        }


