from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import *
from checklist.models import Checklists
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SubmitApplicationForm, ExpertiseDetail
from django.contrib import messages
import os
from django.core.files.base import ContentFile

from pdfminer.high_level import extract_text
import nltk
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from pymystem3 import Mystem
import pymystem3
from nltk.probability import FreqDist
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import re
import io
from .filters import CasesFilter
from django_filters.views import FilterView
import pymorphy2
import docx

import asyncio

from django.http.response import HttpResponse
from django.utils.decorators import classonlymethod
from asgiref.sync import sync_to_async
import threading


class SubmitApplication(LoginRequiredMixin, CreateView):
    model = Cases
    template_name = 'case/submit_application.html'
    form_class = SubmitApplicationForm
    context_object_name = 'case'
    success_url = reverse_lazy('expertise')
    login_url = reverse_lazy('login')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SubmitApplication, self).get_context_data(**kwargs)
        context['title'] = 'Подать заявку'
        return context

    def get_form_kwargs(self):
        kwargs = super(SubmitApplication, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()

        if self.request.user.is_staff:
            self.object.payer = form.cleaned_data.get("payer")
        else:
            self.object.payer = self.request.user


        rep = Documents.objects.create(case=self.object, file=self.request.FILES['report'],
                                       type=DocumentTypes.objects.get(title='Отчёт'))


        dec = Documents.objects.create(case=self.object, file=self.request.FILES['declaration'],
                                 type=DocumentTypes.objects.get(title='Декларация'))
        if 'specification' in self.request.FILES:
            spec = Documents.objects.create(case=self.object, file=self.request.FILES['specification'],
                                     type=DocumentTypes.objects.get(title='Техническое задание'))
            ch = Checklists.objects.create(case=self.object, report=rep, specification = spec, declaration = dec)
        else:
            ch = Checklists.objects.create(case=self.object, report=rep, declaration = dec)


        messages.success(self.request, 'Заявка успешно отправлена.')


        Messages.objects.create(case=self.object, text=self.object.status)


        def async_function():

            def getText(filename):  # Функция для получения текста документа формата .docx
                document = docx.Document(filename)
                fullText = []
                for para in document.paragraphs:
                    fullText.append(para.text)
                return '\n'.join(fullText)

            _, file_extension = os.path.splitext(ch.report.file.path)
            if file_extension == '.pdf':
                text = extract_text(ch.report.file.path)
            elif file_extension == '.docx':
                text = getText(ch.report.file.path)

            text = text.lower()
            nltk.download("stopwords")
            punctuation = string.punctuation
            text = remove_chars_from_text(text, punctuation)
            text = remove_chars_from_text(text, string.digits)
            text_bin = text

            tokenizer = RegexpTokenizer(r'\w+')
            text = tokenizer.tokenize(text)
            text = [i for i in text if i not in stopwords.words('russian')]
            text = [i for i in text if i not in stopwords.words('english')]

            mystem_analyzer = Mystem()
            text = ' '.join([str(elem) for elem in text])
            text = mystem_analyzer.lemmatize(text)
            text = [w for w in text if (w != ' ')]
            text = nltk.Text(text)
            res = FreqDist(text)
            f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/documents/dict.txt'), encoding='utf-8')
            our_dict = []
            for line in f:
                our_dict.append(line[:-1])
            vocab = {}
            for k in our_dict:
                vocab[k] = text.count(k)

            sorted_dict = {}
            sorted_keys = sorted(vocab, key=vocab.get, reverse=True)

            for w in sorted_keys:
                sorted_dict[w] = vocab[w]


            data = pd.DataFrame.from_dict(sorted_dict, orient='index', columns=['counts'])
            data_30 = data.head(30)


            plt.figure(figsize=(26, 8))
            sns.barplot(data=data_30, x=(data_30.index), y=(data_30.counts))
            plt.xticks(rotation=45, fontsize=15)
            plt.yticks(fontsize=20)
            plt.ylabel('Количество', fontsize=20)

            buffer2 = BytesIO()
            plt.savefig(buffer2, bbox_inches='tight')
            content_file2 = ContentFile(buffer2.getvalue())
            ch.report_diagram.save('diagramm', content_file2)


            for i in ['цель', 'содержание', 'введение', 'основная часть', 'заключение', 'список исполнителей',
                      'список источников|список использованных источников|список использованной литературы|список литературы',
                      'приложение']:
                if (len(re.findall('\n {0,100}' + str(i) + ' {0,100}\n', text_bin)) >= 1):
                    if str(i) == 'цель':
                        ch.has_purpose = True
                        ch.save(update_fields=["has_purpose"])
                    if str(i) == 'содержание':
                        ch.has_content = True
                        ch.save(update_fields=["has_content"])

                    if str(i) == 'введение':
                        ch.has_introduction = True
                        ch.save(update_fields=["has_introduction"])

                    if str(i) == 'основная часть':
                        ch.has_main_part = True
                        ch.save(update_fields=["has_main_part"])

                    if str(i) == 'заключение':
                        ch.has_conclusion = True
                        ch.save(update_fields=["has_conclusion"])

                    if str(i) == 'список исполнителей':
                        ch.has_performers = True
                        ch.save(update_fields=["has_performers"])

                    if str(i) == 'список источников|список использованных источников|список использованной литературы|список литературы':
                        ch.has_sources = True
                        ch.save(update_fields=["has_sources"])
                    if str(i) == 'приложение':
                        ch.has_application = True
                        ch.save(update_fields=["has_application"])

            _, file_extension = os.path.splitext(ch.report.file.path)
            if file_extension == '.pdf':
                file = extract_text(ch.report.file.path)
            elif file_extension == '.docx':
                file = getText(ch.report.file.path)




            def create_df(file):
                file = file.lower()
                text_bin = file
                tokenizer = RegexpTokenizer(r'\w+')
                text = tokenizer.tokenize(file)

                text = [i for i in text if i not in stopwords.words('russian')]
                text = [i for i in text if i not in stopwords.words('english')]

                file = remove_chars_from_text(file, string.punctuation)
                file = remove_chars_from_text(file, string.digits)

                text = ' '.join([str(elem) for elem in text])
                nltk.download('punkt')
                text_tokens = word_tokenize(text)
                text = nltk.Text(text_tokens)
                fdist = FreqDist(text)
                df = pd.DataFrame(fdist.items(), columns=['word', 'count'])
                return text_bin, df

            text, df = create_df(file)

            def words_2(df):
                morph = pymorphy2.MorphAnalyzer()
                for i in range(len(df)):
                    df.word[i] = morph.parse(df.word[i])[0].normal_form
                new_words = df.groupby(by=df.word, sort=False, as_index=False).sum()
                return new_words

            new_df = words_2(df)
            data_words = pd.read_excel(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/documents/dict_excel.xlsx'))

            topics = {}
            for col in data_words:
                tmp = data_words[col]
                topics[col] = new_df.merge(tmp, how='inner', left_on='word', right_on=col)['count'].sum()

            result_topic = max(topics, key=topics.get)
            ch.section_analyze = result_topic
            ch.save(update_fields=["section_analyze"])

        threading.Thread(target=async_function).start()

        print('ASYNC STARTED!')


        self.object.status = CaseStatus.objects.get(code=2)
        Messages.objects.create(case=self.object, text=self.object.status)

        self.object.status = CaseStatus.objects.get(code=3)
        Messages.objects.create(case=self.object, text=self.object.status)

        return super().form_valid(form)


def remove_chars_from_text(text, chars):
    return "".join([ch for ch in text if ch not in chars])


class Notifications(LoginRequiredMixin, ListView):
    model = Messages
    template_name = 'case/messages.html'
    context_object_name = 'messages'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        c = Cases.objects.filter(payer=self.request.user)
        return Messages.objects.filter(case__in=c).order_by('-case', '-added')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Notifications, self).get_context_data(**kwargs)
        context['title'] = 'Сообщения'
        return context


class Expertise(LoginRequiredMixin, ListView):
    model = Cases
    template_name = 'case/expertise.html'
    context_object_name = 'expertise'
    login_url = reverse_lazy('login')
    filterset_class = CasesFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            queryset = Cases.objects.all().order_by('-opened')
        else:
            queryset = Cases.objects.filter(payer=self.request.user).order_by('-opened')

        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Expertise, self).get_context_data(**kwargs)
        context['title'] = 'Экспертизы'
        context['filterset'] = self.filterset

        return context


class ExpertiseDetail(LoginRequiredMixin, DetailView):
    model = Cases
    template_name = 'case/expertise_detail.html'
    form_class = ExpertiseDetail
    context_object_name = 'expertise'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ExpertiseDetail, self).get_context_data(**kwargs)
        context['title'] = 'Экспертизы'
        return context

    def get_object(self):
        return get_object_or_404(Cases, number=self.kwargs.get("expertise_number"))
