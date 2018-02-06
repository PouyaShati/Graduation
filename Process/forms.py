from django import forms

from .models import Process_Blueprint, Question_Set, Employee_Task_Blueprint, Question
from django.utils.translation import ugettext_lazy as _


class CreateProcessBlueprintForm(forms.ModelForm):
    class Meta:
        model = Process_Blueprint
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'نام پروسه',
                                                'style': 'text-align:right'})
        }

        labels = {
            'name': _('نام پروسه'),
        }

        # TODO add preprocesses

        '''
        for process_bp in Process_Blueprint.objects.all():
            key = 'preprocess_' + process_bp.name
            fields.append(key)
            widgets[key] = forms.NullBooleanSelect(attrs={'class': 'form-control'})
            labels[key] = _('Requires ' + process_bp.name)
        '''


class CreateQuestionSetForm(forms.ModelForm): # TODO add the ability to enter multiple questions
    '''
    class Meta:
        model = Question_Set
        fields = ['question1', 'question2', 'question3', 'question1_type', 'question2_type', 'question3_type']

        choices = [
        ('Text','Text'),
        ('Integer','Integer'),
        ('Real','Real'),
        ('Document','Document'),
        ('Multiple Choice','Multiple Choice'),] # connecting this to Question's set of choices directly

        widgets = {
            'question1': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'سوال اول',
                                           'style': 'text-align:right'}),
            'question2': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'سوال دوم',
                                                'style': 'text-align:right'}),
            'question3': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'سوال سوم',
                                                'style': 'text-align:right'}),
            'question1_type': forms.SelectMultiple(choices=choices, attrs={'class': 'form-control'}),
            'question2_type': forms.SelectMultiple(choices=choices, attrs={'class': 'form-control'}),
            'question3_type': forms.SelectMultiple(choices=choices, attrs={'class': 'form-control'}),
        }

        labels = {
            'question1': _('سوال اول'),
            'question2': _('سوال دوم'),
            'question3': _('سوال سوم'),
            'question1_type': _('نوع سوال اول'),
            'question2_type': _('نوع سوال دوم'),
            'question3_type': _('نوع سوال سوم'),
        }
    '''
    class Meta:
        model = Question_Set
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'نام مجموعه سوال',
                                           'style': 'text-align:right'})
        }


class CreateEmployeeTaskBlueprintForm(forms.ModelForm): # TODO add fields default_of and question_set that return instances of classes Process_Blueprint and Question_Set

    class Meta:
        model = Employee_Task_Blueprint
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'نام وظیفه کارمند',
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


class AddPreprocessForm(forms.ModelForm): # TODO field name should be of type Process_Blueprint
    class Meta:
        model = Question
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'نام پروسه',
                                                   'style': 'text-align:right'}),

        }
        labels = {
            'name': _('نام پروسه'),
        }