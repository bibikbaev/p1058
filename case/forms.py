from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import *
from django import forms
import datetime


class DateInput(forms.DateInput):
    input_type = 'date'


class SubmitApplicationForm(forms.ModelForm):
    declaration = forms.FileField(label='Декларация', widget=forms.FileInput(attrs={'class': 'form-control'}))
    report = forms.FileField(label='Отчёт', widget=forms.FileInput(attrs={'class': 'form-control'}))
    specification = forms.FileField(label='Техническое задание', required=False,
                                    widget=forms.FileInput(attrs={'class': 'form-control'}))
    sp_checkbox = forms.BooleanField(label='Нет', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'gridCheck'}))

    class Meta:
        model = Cases
        fields = ('title', 'theme', 'type', 'start_job', 'end_job', 'payer')
        widgets = {
            'start_job': DateInput(),
            'end_job': DateInput(),
        }


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['payer'].widget.attrs.update({'required':False, 'class': 'form-control'})
        self.fields['payer'].queryset = CustomUser.objects.filter(role=1, is_staff=False)

        self.fields['title'].widget.attrs.update({'required':True, 'class': 'form-control'})
        self.fields['theme'].widget.attrs.update({'required':True, 'class': 'form-control'})
        self.fields['type'].widget.attrs.update({'required':True, 'class': 'form-control'})
        self.fields['start_job'].widget.attrs.update({'class': 'form-control'})
        self.fields['end_job'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_job'].widget.attrs.update({'required':True, 'min': '2010-01-01', 'max': datetime.date.today()})
        self.fields['end_job'].widget.attrs.update({'required':True, 'min': '2010-01-01', 'max': datetime.date.today()})


        if self.user.is_staff:
            self.fields['payer'].required = True

    def clean(self):
        sdate = self.cleaned_data['start_job']
        edate = self.cleaned_data['end_job']
        if sdate > edate:
            raise forms.ValidationError('Дата начала работ не может быть больше даты окончания.')
        if sdate > datetime.date.today():
            raise forms.ValidationError('Дата начала работ не может быть больше текущей даты.')
        if edate > datetime.date.today():
            raise forms.ValidationError('Дата окончания работ не может быть больше текущей даты.')

        check = [self.cleaned_data['specification'], self.cleaned_data['sp_checkbox']]
        if any(check) and not all(check):
            return self.cleaned_data
        raise ValidationError('Необходимо загрузить техническое задание либо отметить, что его нет.')


class ExpertiseDetail(forms.ModelForm):
    class Meta(object):
        model = Cases
        fields = ('__all__')


class MessagesList(forms.ModelForm):
    class Meta(object):
        model = Messages
        fields = ('__all__')