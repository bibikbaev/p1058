from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import MaxLengthValidator, MinLengthValidator
from .models import CustomUser


class RegisterUserForm(UserCreationForm):
    title = forms.CharField(label='Название компании', widget=forms.TextInput(attrs={'class': 'form_field', 'autocomplete': 'off'}))
    inn = forms.CharField(required=True, max_length=11, min_length=11, label='ИНН', widget=forms.TextInput(attrs={'placeholder':'ИНН компании из 11 цифр', 'name':'inn', 'id': 'inn', 'class': 'form_field', 'autocomplete': 'off','pattern':'[0-9]+', 'title':'ИНН должен содержать только цифры'}),
                          validators=[MinLengthValidator(11, message="ИНН должен состоять из 11 цифр."),
                                      MaxLengthValidator(11, message="ИНН должен состоять из 11 цифр.")])

    kpp = forms.CharField(max_length=9, min_length=9, label='КПП', widget=forms.TextInput(attrs={'placeholder':'КПП компании из 9 цифр', 'id': 'kpp', 'class': 'form_field',  'autocomplete': 'off','pattern':'[0-9]+', 'title':'КПП должен содержать только цифры'}),
                          validators=[MinLengthValidator(9, message="КПП должен состоять из 9 цифр."),
                                      MaxLengthValidator(9, message="КПП должен состоять из 9 цифр.")])
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'id': 'email', 'class': 'form_field'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'id': 'password1', 'class': 'form_field'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'id': 'password2', 'class': 'form_field'}))

    class Meta:
        model = CustomUser
        fields = ('title', 'inn', 'kpp', 'email', 'password1', 'password2')


class RegisterEmpForm(UserCreationForm):
    inn = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder':'Логин для входа', 'class': 'form_field'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder':'Email', 'class': 'form_field'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'placeholder':'Фамилия', 'class': 'form_field'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'placeholder':'Имя', 'class': 'form_field'}))
    middle_name = forms.CharField(label='Отчество', widget=forms.TextInput(attrs={'placeholder':'Отчество', 'class': 'form_field'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder':'Пароль', 'class': 'form_field'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'placeholder':'Повтор пароля', 'class': 'form_field'}))

    class Meta:
        model = CustomUser
        fields = ('inn', 'email', 'password1', 'password2', 'last_name', 'first_name', 'middle_name')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин (ваш ИНН)',
                               widget=forms.TextInput(attrs={'placeholder':'Логин (Ваш ИНН)', 'class': 'form_field'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'placeholder':'Пароль', 'class': 'form_field'}))


class LoginUserForm1(AuthenticationForm):
    username = forms.CharField(label='Логин (ваш ИНН)',
                               widget=forms.TextInput(attrs={'class':'form_field'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class':'form_field'}))


class ProfileUserForm(forms.ModelForm):
    class Meta(object):
        model = CustomUser
        fields = ('email', 'phone', 'title', 'inn', 'kpp', 'head_full_name', 'chief_accountant_full_name', 'first_name', 'last_name', 'middle_name')

    def __init__(self, *args, **kwargs):
        super(ProfileUserForm, self).__init__(*args, **kwargs)
        self.fields['title'].disabled = True
        self.fields['inn'].disabled = True
        self.fields['kpp'].disabled = True
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['inn'].widget.attrs.update({'class': 'form-control'})
        self.fields['kpp'].widget.attrs.update({'class': 'form-control'})
        self.fields['head_full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['chief_accountant_full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['middle_name'].widget.attrs.update({'class': 'form-control'})
