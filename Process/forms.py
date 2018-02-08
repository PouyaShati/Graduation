from django import forms

from .models import Process_Blueprint, Question_Set, Employee_Task_Blueprint, Question, Form_Blueprint, Payment_Blueprint
from django.utils.translation import ugettext_lazy as _


class CreateProcessBlueprintForm(forms.ModelForm):
    class Meta:
        model = Process_Blueprint
        fields = ['name', 'department']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'نام پروسه',
                                                'style': 'text-align:right'}),
            'department' : forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'نام دپارتمان',
                                                'style': 'text-align:right'}),
        }

        labels = {
            'name': _('نام پروسه'),
            'department': _('نام دپارتمان'),
        }
        error_messages = {
            'name': {'required': _('لطفا نام پروسه را وارد کنید')},
            'department': {'required': _('لطفا شماره دپارتمان را وارد کنید'),
                           'invalid_choice': _('چنین دپارتمانی موجود نیست')}
        }


class AddPreprocessForm(forms.Form):
    name = forms.RegexField(regex=r'^\w+$',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'required': 'True',
                                                              'max_length': 30,
                                                              'placeholder': 'نام فرایند پیشنیاز',
                                                              'style': 'text-align:right'}
                                                       ),
                                label=_("نام فرایند پیشنیاز"),
                                error_messages={
                                    'required': _('نام فرایند پیشنیاز را وارد کنید'),
                                    'invalid': _("نام باید فقط شامل حروف، اعداد و _ باشد")})

class CreateEmployeeTaskBlueprintForm(forms.ModelForm):
    class Meta:
        model = Employee_Task_Blueprint
        fields = ['name', 'question_set']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'نام وظیفه کارمند',
                                           'style': 'text-align:right'}),
            'question_set':  forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'مجموعه سوال',
                                           'style': 'text-align:right'})
        }
        labels = {'name': _('نام وظیفه کارمند'), 'question_set': _('مجموعه سوال')}
        error_messages = {
            'name': {'required': _('نام وظیفه کارمند را وارد کنید')},
            'question_set': {'required': _('مجموعه سوال را وارد کنید'),
                             'invalid_choice': _('چنین مجموعه سوالی موجود نیست')}
        }

class CreateFormBlueprintForm(forms.ModelForm):
    class Meta:
        model = Form_Blueprint
        fields = ['name', 'question_set', 'is_timed', 'max_time'] #TODO what is name?
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'نام وظیفه کارمند',
                                           'style': 'text-align:right'}),
            'question_set': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'مجموعه سوال',
                                           'style': 'text-align:right'}),
            'is_timed': forms.CheckboxInput(attrs={'class': 'form-control',
                                                   'placeholder': 'زمانی',
                                                   'style': 'text-align:right'
                                                  }),
            'max_time': forms.NumberInput(attrs={'class': 'form-control',
                                                   'placeholder': 'حداکثر زمان',
                                                   'style': 'text-align:right'
                                                })
        }
        labels = {'name': _('نام وظیفه کارمند'), 'question_set': _('مجموعه سوال'),
                  'is_timed': _('زمانی'), 'max_time': _('حداکثر زمان')}
        error_messages = {'name': {'required': _('نام وظیفه کارمند را وارد کنید')},
                          'question_set': {'required': _('مجموعه سوال را وارد کنید'),
                                           'invalid_choice': _('چنین مجموعه سوالی وجود ندارد')}}
        #TODO if is_timed is check, max_time should be mandatory



class CreatePaymentBlueprintForm(forms.ModelForm):
    class Meta:
        model = Payment_Blueprint
        fields = ['name', 'default_amount', 'is_timed', 'max_time'] #TODO what is name?
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'نام وظیفه کارمند',
                                           'style': 'text-align:right'}),
            'default_amount': forms.NumberInput(attrs={'class': 'form-control',
                                           'placeholder': 'مقدار پیشفرض',
                                           'style': 'text-align:right'
                                                       }),
            'is_timed': forms.CheckboxInput(attrs={'class': 'form-control',
                                                   'placeholder': 'زمانی',
                                                   'style': 'text-align:right'
                                                  }),
            'max_time': forms.NumberInput(attrs={'class': 'form-control',
                                                   'placeholder': 'حداکثر زمان',
                                                   'style': 'text-align:right'
                                                })
        }
        labels = {'name': _('نام وظیفه کارمند'), 'default_amount': _('مقدار پیشفرض'),
                  'is_timed': _('زمانی'), 'max_time': _('حداکثر زمان')}
        error_messages = {'name': {'required': _('نام وظیفه کارمند را وارد کنید')},
                          'default_amount': {'required': _('مجموعه سوال را وارد کنید'),
                                           'invalid_choice': _('چنین مجموعه سوالی وجود ندارد')}}
        #TODO if is_timed is check, max_time should be mandatory
        #TODO shouldnt we have receiver?


class CreateQuestionSetForm(forms.ModelForm):
    class Meta:
        model = Question_Set
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'نام مجموعه سوال',
                                           'style': 'text-align:right'})
        }
        labels = {'name': _('نام مجموعه سوال')}
        error_messages = {'name': {'required': 'نام مجموعه سوال را وارد کنید'}}


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'type']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'متن سوال',
                                                   'style': 'text-align:right'}),
            'type': forms.Select(attrs={'class': 'form-control',
                                              'placeholder': 'نوع سوال',
                                              'style': 'text-align:right'}),

        }
        labels = {
            'text': _('متن سوال'),
            'type': _('نوع سوال'),
        }
        error_messages = {
            'text': {
                'required': _('متن سوال را وارد کنید')
            },
            'type': {
                'required': _('نوع سوال را وارد کنید')
            }
        }