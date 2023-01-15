from .models import *
from django import forms
import datetime


class DateInput(forms.DateInput):
    input_type = 'date'


class ChecklistDetail(forms.ModelForm):
    has_performers = forms.BooleanField(label='Есть список исполнителей', required=False,
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    has_introduction = forms.BooleanField(label='Есть введение', required=False,
                                          widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    has_conclusion = forms.BooleanField(label='Есть заключение', required=False,
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    has_application = forms.BooleanField(label='Есть приложения', required=False,
                                         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    has_content = forms.BooleanField(label='Есть содержание', required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    has_sources = forms.BooleanField(label='Есть список источников', required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    has_main_part = forms.BooleanField(label='Есть основная часть', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    adopted = forms.BooleanField(label='Принять работу', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    comment = forms.CharField(label='Комментарий от инспектора', required=False,
                              widget=forms.Textarea(attrs={'class': 'form-control'}))
    class Meta(object):
        model = Checklists
        fields = ('has_content', 'has_introduction', 'has_main_part', 'has_conclusion', 'has_performers', 'has_sources',
                  'has_application', 'adopted', 'comment')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ChecklistDetail, self).__init__(*args, **kwargs)

        if not self.user.is_staff:
            for f in self.fields:
                self.fields[f].disabled = True

        self.fields['has_content'].disabled = True
        self.fields['has_introduction'].disabled = True
        self.fields['has_main_part'].disabled = True
        self.fields['has_conclusion'].disabled = True
        self.fields['has_performers'].disabled = True
        self.fields['has_sources'].disabled = True
        self.fields['has_application'].disabled = True


class ChecklistDetailMain(forms.ModelForm):
    user_has_performers = forms.BooleanField(label='Есть список исполнителей', required=False,
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    user_has_introduction = forms.BooleanField(label='Есть введение', required=False,
                                          widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    user_has_conclusion = forms.BooleanField(label='Есть заключение', required=False,
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    user_has_application = forms.BooleanField(label='Есть приложения', required=False,
                                         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    user_has_content = forms.BooleanField(label='Есть содержание', required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    user_has_sources = forms.BooleanField(label='Есть список источников', required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    user_has_main_part = forms.BooleanField(label='Есть основная часть', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))


    udk_index = forms.CharField(label='Индекс УДК по ГОСТ 7.90', required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    numbers_report_ident = forms.CharField(label='Номера, идентифицирующие отчет', required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    report_type = forms.CharField(label='Вид отчета', required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    nir_maker = forms.CharField(label='Фамилии и инициалы исполнителей НИР', required=False,
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    maker_post = forms.CharField(label='Должности исполнителей НИР', required=False,
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    maker_degree = forms.CharField(label='Ученые степени исполнителей НИР', required=False,
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    maker_title = forms.CharField(label='Ученые звания исполнителей НИР', required=False,
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))

    report_place = forms.CharField(label='Место составления отчета', required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    page_count = forms.IntegerField(label='Количество страниц', required=False,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))

    application_count = forms.IntegerField(label='Количество приложений', required=False,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))

    source_count = forms.IntegerField(label='Количество использованных источников', required=False,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))

    key_words = forms.CharField(label='Перечень ключевых слов', required=False,
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))

    is_gost = forms.BooleanField(label='Отчет о НИОКР и иные первичные документы, подтверждающие процесс и объем выполненных работ, оформлены в соответствии с ГОСТами - ГОСТ 15.101-98, ГОСТ 7.32-2001', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_first = forms.BooleanField(label='Выполненные работы являются впервые разработанными, имеют научно-техническую новизну', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_unique = forms.BooleanField(label='Выполненные работы направлены на создание нового уникального продукта, знания или решения', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    exp_desc = forms.BooleanField(label='В тематической области выполненных работ отсутствовал накопленный в российской или мировой практике опыт решения аналогичных инженерно-технических задач и его описания в открытых источниках', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    contain_unique = forms.BooleanField(label='Выполненные работы содержат в качестве предмета или объекта труда уникальные и (или) инновационные инструменты, материалы, оборудование, подходы, процессы, источники энергии и др.', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    contain_experiment = forms.BooleanField(label='Выполненные работы содержат в себе признаки экспериментальных разработок и предполагают проведение реальных исследований', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    efficient_nec = forms.BooleanField(label='Выполненные работы не обусловлены необходимостью повышения эффективности операционной деятельности телекоммуникационных компаний', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    integration = forms.BooleanField(label='Выполненные работы не характерны для типового внедренческого проекта по системной интеграции существующих решений', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    risk = forms.BooleanField(label='Выполненные работы имели высокие проектные и технологические риски, в целях снижения которых исполнители создавали компетенций, прототипы, математические и натурные модели, макеты, лабораторные образцы будущего изделия', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    used = forms.BooleanField(label='Разработанные / примененные решения не основаны на общеизвестных способах, методах, принципах и (или) технологиях по совокупности функциональных свойств, широко используемых в различных отраслях науки', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    union = forms.BooleanField(label='Выполненные работы не являются объединением общеизвестных технологий и алгоритмов', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    modification = forms.BooleanField(label='В ходе выполнения работ не осуществлялась настройка/ доработка/ модификация ранее известных технологий, алгоритмов и принципов функционирования систем, разработанных с применением общеизвестных методов и алгоритмов', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    analog = forms.BooleanField(label='В отношении предлагаемого решения не существуют общедоступные аналоги по совокупности функциональных свойств, решающих подобные задачи', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    new_knowledge = forms.BooleanField(label='Выполненные работы не являются решением технических или инженерных задач по адаптации решения для работы в виртуальной среде, в ходе реализации требовали проведение научных исследований и привели к получению новых знаний', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ChecklistDetailMain, self).__init__(*args, **kwargs)
        self.fields['report_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['report_date'].widget.attrs.update({'required':False, 'min': '2010-01-01', 'max': datetime.date.today()})


    class Meta(object):
        model = Checklists
        widgets = {
            'report_date': DateInput(),
        }
        fields = ('is_gost', 'user_has_content', 'user_has_introduction', 'user_has_main_part', 'user_has_conclusion', 'user_has_performers', 'user_has_sources',
                  'user_has_application', 'udk_index', 'numbers_report_ident', 'report_date', 'report_type', 'nir_maker', 'maker_post', 'maker_degree',
                  'maker_title', 'report_place', 'page_count', 'application_count', 'source_count', 'key_words', 'is_first', 'is_unique',
                  'exp_desc', 'contain_unique', 'contain_experiment', 'efficient_nec', 'integration', 'risk', 'used', 'union', 'modification',
                  'analog', 'new_knowledge')
