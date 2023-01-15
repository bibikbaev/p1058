from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import *
from case.models import Cases, CaseStatus, Messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ChecklistDetail, ChecklistDetailMain
from django.contrib import messages
from django.http import HttpResponse


class ChecklistDetail(LoginRequiredMixin, UpdateView):
    model = Checklists
    template_name = 'checklist/checklist_detail.html'
    form_class = ChecklistDetail
    context_object_name = 'checklist'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChecklistDetail, self).get_context_data(**kwargs)
        context['title'] = 'Чек-лист'
        return context

    def get_object(self):
        c = Cases.objects.get(number=self.kwargs.get("ch_number"))
        return get_object_or_404(Checklists, case=c)

    def get_form_kwargs(self):
        kwargs = super(ChecklistDetail, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        c = Cases.objects.get(number=self.kwargs.get("ch_number"))
        c.status = CaseStatus.objects.get(code=4)
        c.save(update_fields=["status"])

        Messages.objects.create(case=c, text=c.status)

        if form.cleaned_data.get("adopted") == True:
            Messages.objects.create(case=c, text='Работа принята')

        if form.cleaned_data.get("adopted") == False:
            Messages.objects.create(case=c, text='Работа отклонена')

        if form.cleaned_data.get("comment"):
            Messages.objects.create(case=c, text='Комментарий от налогового инспектора: ' + form.cleaned_data.get("comment"))


        return super().form_valid(form)


def handler500(request, exception=None):
    return render(request, "checklist/500.html", {})



class ChecklistDetailMain(LoginRequiredMixin, UpdateView):
    model = Checklists
    template_name = 'checklist/checklist_main.html'
    form_class = ChecklistDetailMain
    context_object_name = 'checklist'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChecklistDetailMain, self).get_context_data(**kwargs)
        context['title'] = 'Чек-лист'
        return context

    def get_object(self):
        c = Cases.objects.get(number=self.kwargs.get("ch_number"))
        return get_object_or_404(Checklists, case=c)

    def get_form_kwargs(self):
        kwargs = super(ChecklistDetailMain, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
