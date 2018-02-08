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


class AddPreprocessForm(forms.Form):
    name = forms.RegexField(regex=r'^\w+$',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'required': 'True',
                                                              'max_length': 30,
                                                              'placeholder': 'preprocess name',
                                                              'style': 'text-align:right'}
                                                       ),
                                label=_("preprocess name"),
                                error_messages={
                                    'invalid': _("This value must contain only letters, numbers and underscores.")})

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

class CreateFormBlueprintForm(forms.ModelForm):
    class Meta:
        model = Form_Blueprint
        fields = ['name', 'question_set', 'is_timed', 'max_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'نام وظیفه کارمند',
                                           'style': 'text-align:right'}),
            'question_set': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'مجموعه سوال',
                                           'style': 'text-align:right'}),
            'is_time': forms.CheckboxInput(attrs={'class': 'form-control',
                                                   #'placeholder': 'مجموعه سوال',
                                                   #'style': 'text-align:right'
                                                  }),
            'max_time': forms.NumberInput(attrs={'class': 'form-control',
                                                   #'placeholder': 'مجموعه سوال',
                                                   #'style': 'text-align:right'
                                                })
        }


class CreatePaymentBlueprintForm(forms.ModelForm):
    class Meta:
        model = Payment_Blueprint
        fields = ['name', 'default_amount', 'is_timed', 'max_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'نام وظیفه کارمند',
                                           'style': 'text-align:right'}),
            'default_amount': forms.NumberInput(attrs={'class': 'form-control',
                                           #'placeholder': 'مجموعه سوال',
                                           #'style': 'text-align:right'
                                                       }),
            'is_time': forms.CheckboxInput(attrs={'class': 'form-control',
                                                   #'placeholder': 'مجموعه سوال',
                                                   #'style': 'text-align:right'
                                                  }),
            'max_time': forms.NumberInput(attrs={'class': 'form-control',
                                                   #'placeholder': 'مجموعه سوال',
                                                   #'style': 'text-align:right'
                                                })
        }



class CreateQuestionSetForm(forms.ModelForm):
    class Meta:
        model = Question_Set
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'نام مجموعه سوال',
                                           'style': 'text-align:right'})
        }


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