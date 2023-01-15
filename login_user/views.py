from django.http import HttpResponseNotFound
from login_user.forms import RegisterUserForm, LoginUserForm, ProfileUserForm, RegisterEmpForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from .models import CustomUser

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'login_user/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RegisterUser, self).get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class RegisterEmp(CreateView):
    form_class = RegisterEmpForm
    template_name = 'login_user/register_emp.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RegisterEmp, self).get_context_data(**kwargs)
        context['title'] = 'Регистрация сотрудника'
        return context

    def form_valid(self, form):
        user = CustomUser.objects.create_user(role=2,
                                              inn=form.cleaned_data['inn'],
                                              email=form.cleaned_data['email'],
                                              password=form.cleaned_data['password1'],
                                              last_name=form.cleaned_data['last_name'],
                                              first_name=form.cleaned_data['first_name'],
                                              middle_name=form.cleaned_data['middle_name'])
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login_user/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'login_user/home.html', {'title': 'Главная страница'})


class ShowProfile(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'login_user/profile.html'
    form_class = ProfileUserForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShowProfile, self).get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        return context

    def get_object(self):
        return get_object_or_404(CustomUser, inn=self.request.user.inn)

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile')


