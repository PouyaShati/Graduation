from django import forms

from .models import Process_Blueprint, Question_Set, Employee_Task_Blueprint, Question, Form_Blueprint, Payment_Blueprint, Task_Blueprint
from django.utils.translation import ugettext_lazy as _
from Employee.models import Department



class CreateProcessBlueprintOperatorForm(forms.ModelForm):
    class Meta:
        model = Process_Blueprint
        fields = ['name', 'department']

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'نام پروسه',
                                                'style': 'text-align:right',
                                                         'direction': 'rtl'}),
                        label=_('نام پروسه'),
                                          error_messages={'required': _('نام پروسه را انتحاب کنید')})

    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(
                                                     attrs={'class': 'form-control',
                                                            'placeholder': 'نام دپارتمان',
                                                            'style': 'text-align:right',
                                                            'direction': 'rtl'}),
                                        label=_('نام دپارتمان'),
                                          error_messages={'required': _('نام دپارتمان را انتخاب کنید')})

class CreateProcessBlueprintForm(forms.ModelForm):
    class Meta:
        model = Process_Blueprint
        fields = ['name']
    #     widgets = {
    #         'name': forms.TextInput(attrs={'class': 'form-control',
    #                                             'placeholder': 'نام پروسه',
    #                                             'style': 'text-align:right'}),
    #         'department': forms.TextInput(attrs={'class': 'form-control',
    #                                             'placeholder': 'کد دپارتمان',
    #                                             'style': 'text-align:right'}),
    #         'department': forms.Select(choices=Department.objects.all().)
    #     }
    #
    #     labels = {
    #         'name': _('نام پروسه'),
    #         'department': _('کد دپارتمان'),
    #     }
    #     error_messages = {
    #         'name': {'required': _('لطفا نام پروسه را وارد کنید')},
    #         'department': {'required': _('لطفا شماره دپارتمان را وارد کنید'),
    #                        'invalid_choice': _('چنین دپارتمانی موجود نیست')}
    #     }
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'نام پروسه',
                                                'style': 'text-align:right',
                                                         'direction': 'rtl'}),
                        label=_('نام پروسه'),
                                          error_messages={'required': _('نام پروسه را انتحاب کنید')})

    # department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(
    #                                                  attrs={'class': 'form-control',
    #                                                         'placeholder': 'نام دپارتمان',
    #                                                         'style': 'text-align:right',
    #                                                         'direction': 'rtl'}),
    #                                     label=_('نام دپارتمان'),
    #                                       error_messages={'required': _('نام دپارتمان را انتخاب کنید')})


class AddPreprocessForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Process_Blueprint.objects.all(),
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


class AddDefaultEmployeeTaskForm(forms.Form):
    employee_task_bp_name = forms.ModelChoiceField(queryset=Employee_Task_Blueprint.objects.all(),
                                widget=forms.Select(attrs={'class': 'form-control',
                                                              'required': 'True',
                                                              'max_length': 30,
                                                              'placeholder': 'نام الگوی وظیفه کارمند پیشفرض',
                                                              'style': 'text-align:right',
                                                              'placeholder': 'نام وظیفه پیشفرض',
                                                              'style': 'text-align:right',
                                                           'direction': 'rtl'}
                                                       ),
                                label=_('نام الگوی وظیفه کارمند پیشفرض'),
                                error_messages={
                                    'required': _('نام وظیفه پیشفرض را وارد کنید'),
                                    'invalid': _("نام باید فقط شامل حروف، اعداد و _ باشد")})
class AddDefaultFormBlueprintTaskForm(forms.Form):
    form_bp_name = forms.ModelChoiceField(queryset=Form_Blueprint.objects.all(),
                                widget=forms.Select(attrs={'class': 'form-control',
                                                              'required': 'True',
                                                              'max_length': 30,
                                                              'placeholder': 'نام الگوی فرم پیشفرض',
                                                              'style': 'text-align:right'}
                                                       ),
                                label=_('نام الگوی فرم پیشفرض'),
                                error_messages={
                                    'required': _('نام وظیفه پیشفرض را وارد کنید'),
                                    'invalid': _("نام باید فقط شامل حروف، اعداد و _ باشد")})

class AddDefaultPaymentBlueprintTaskForm(forms.Form):
    payment_bp_name = forms.ModelChoiceField(queryset=Payment_Blueprint.objects.all(),
                                widget=forms.Select(attrs={'class': 'form-control',
                                                              'required': 'True',
                                                              'max_length': 30,
                                                              'placeholder': 'نام الگوی پرداخت پیشفرض',
                                                              'style': 'text-align:right'}
                                                       ),
                                label=_('نام الگوی پرداخت پیشفرض'),
                                error_messages={
                                    'required': _('نام وظیفه پیشفرض را وارد کنید'),
                                    'invalid': _("نام باید فقط شامل حروف، اعداد و _ باشد")})


class CreateEmployeeTaskBlueprintForm(forms.ModelForm):
    class Meta:
        model = Employee_Task_Blueprint
        fields = ['name', 'question_set']
    #     widgets = {
    #         'name': forms.TextInput(attrs={'class': 'form-control',
    #                                        'placeholder': 'نام وظیفه کارمند',
    #                                        'style': 'text-align:right'}),
    #         'question_set':  forms.TextInput(attrs={'class': 'form-control',
    #                                        'placeholder': 'مجموعه سوال',
    #                                        'style': 'text-align:right'})
    #     }
    #     labels = {'name': _('نام وظیفه کارمند'), 'question_set': _('مجموعه سوال')}
    #     error_messages = {
    #         'name': {'required': _('نام وظیفه کارمند را وارد کنید')},
    #         'question_set': {'required': _('مجموعه سوال را وارد کنید'),
    #                          'invalid_choice': _('چنین مجموعه سوالی موجود نیست')}
    #     }
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'نام الگوی وظیفه کارمند',
                                                            'style': 'text-align:right',
                                                         'direction': 'rtl'}),
                           label = _('نام الگوی وظیفه کارمند'),
                           error_messages={'required': _('نام الگوی وظیفه کارمند')})
    question_set = forms.ModelChoiceField(queryset=Question_Set.objects.all(), widget=forms.Select(
                                                     attrs={'class': 'form-control',
                                                            'placeholder': 'مجموعه سوال',
                                                            'style': 'text-align:right',
                                                            'direction': 'rtl'}),
                                          label=_('مجموعه سوال'),
                                          error_messages={'required': _('مجموعه سوال را انتحاب کنید')})

class CreateFormBlueprintForm(forms.ModelForm):
    class Meta:
        model = Form_Blueprint
        fields = ['name', 'question_set', 'is_timed', 'max_time'] #TODO what is name?
    #     widgets = {
    #         'name': forms.TextInput(attrs={'class': 'form-control',
    #                                        'placeholder': 'نام وظیفه کارمند',
    #                                        'style': 'text-align:right'}),
    #         'question_set': forms.TextInput(attrs={'class': 'form-control',
    #                                        'placeholder': 'مجموعه سوال',
    #                                        'style': 'text-align:right'}),
    #         'is_timed': forms.CheckboxInput(attrs={'class': 'form-control',
    #                                                'placeholder': 'زمانی',
    #                                                'style': 'text-align:right'
    #                                               }),
    #         'max_time': forms.NumberInput(attrs={'class': 'form-control',
    #                                                'placeholder': 'حداکثر زمان',
    #                                                'style': 'text-align:right'
    #                                             })
    #     }
    #     labels = {'name': _('نام وظیفه کارمند'), 'question_set': _('مجموعه سوال'),
    #               'is_timed': _('زمانی'), 'max_time': _('حداکثر زمان')}
    #     error_messages = {'name': {'required': _('نام وظیفه کارمند را وارد کنید')},
    #                       'question_set': {'required': _('مجموعه سوال را وارد کنید'),
    #                                        'invalid_choice': _('چنین مجموعه سوالی وجود ندارد')}}
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'نام الگوی فرم',
                                                            'style': 'text-align:right',
                                                         'direction': 'rtl'}),
                           label = _('نام الگوی فرم'),
                           error_messages={'required': _('نام الگوی فرم را وارد کنید')})
    question_set = forms.ModelChoiceField(queryset=Question_Set.objects.all(), widget=forms.Select(
                                                     attrs={'class': 'form-control',
                                                            'placeholder': 'مجموعه سوال',
                                                            'style': 'text-align:right',
                                                            'direction': 'rtl'}),
                                          label=_('مجموعه سوال'),
                                          error_messages={'required': _('مجموعه سوال را انتحاب کنید')})
    is_timed = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control',
                                                                  'placeholer': 'زمانی',}),
                                                                  #'style': 'text-align:right'
                                  label= _('زمانی'), required=False)
    max_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholer': 'حداکثر زمان'}),
                                                                      #'style': 'text-align:right'
                                    label= _('حداکثر زمان'), required=False)
        #TODO if is_timed is check, max_time should be mandatory



class CreatePaymentBlueprintForm(forms.ModelForm):
    class Meta:
        model = Payment_Blueprint
        fields = ['name', 'default_amount', 'is_timed', 'max_time', 'receiver'] #TODO what is name?
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'نام الگوی پرداخت',
                                           'style': 'text-align:right',
                                           'direction': 'rtl'}),
            'default_amount': forms.NumberInput(attrs={'class': 'form-control',
                                           'placeholder': 'مقدار پیشفرض'}),
                                           #'style': 'text-align:right'
            'is_timed': forms.CheckboxInput(attrs={'class': 'form-control',
                                                   'placeholder': 'زمانی'}),
                                                   #'style': 'text-align:right'
            'max_time': forms.NumberInput(attrs={'class': 'form-control',
                                                   'placeholder': 'حداکثر زمان'}),
                                                   #'style': 'text-align:right'
            'receiver': forms.NumberInput(attrs={'class': 'form-control',
                                                 'placeholder': 'شماره حساب مقصد'})
                                          #'style': 'text-align:right'
        }
        labels = {'name': _('نام الگوی پرداخت'), 'default_amount': _('مقدار پیشفرض'),
                  'is_timed': _('زمانی'), 'max_time': _('حداکثر زمان'),
                  'receiver': _('شماره حساب مقصد')}
        error_messages = {'name': {'required': _('نام وظیفه کارمند را وارد کنید')},
                          'default_amount': {'required': _('مقدار پیشفرض را وارد کنید'),
                                           'invalid_choice': _('چنین مجموعه سوالی وجود ندارد')},
                          'receiver': {'required': _('شماره حساب مقصد را وارد کنید'),
                                       'invalid': _('شماره حساب معتبر نیست')}}
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
                                                   'style': 'text-align:right',
                                                'direction': 'rtl'}),
            'type': forms.Select(attrs={'class': 'form-control',
                                              'placeholder': 'نوع سوال',
                                              'style': 'text-align:right',
                                                'direction': 'rtl'}),

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