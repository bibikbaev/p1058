# Generated by Django 3.1.4 on 2022-11-03 17:27

import case.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(default=case.models.random_string, max_length=10, verbose_name='Номер дела')),
                ('title', models.CharField(max_length=300, verbose_name='Наименование работы')),
                ('opened', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Открыто')),
                ('closed', models.DateTimeField(blank=True, null=True, verbose_name='Закрыто')),
                ('start_job', models.DateField(blank=True, null=True, verbose_name='Начало выполнения работ')),
                ('end_job', models.DateField(blank=True, null=True, verbose_name='Конец выполнения работ')),
            ],
            options={
                'verbose_name': 'Налоговое дело',
                'verbose_name_plural': 'Налоговые дела',
            },
        ),
        migrations.CreateModel(
            name='CaseStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(blank=True, null=True, verbose_name='Номер')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Статус дела',
                'verbose_name_plural': 'Статусы дел',
            },
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(default=django.utils.timezone.now)),
                ('file', models.FileField(upload_to='documents/%Y/%m/%d/', verbose_name='Файл')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
        migrations.CreateModel(
            name='DocumentStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Статус документа',
                'verbose_name_plural': 'Статусы документов',
            },
        ),
        migrations.CreateModel(
            name='DocumentTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип документа',
                'verbose_name_plural': 'Типы документов',
            },
        ),
        migrations.CreateModel(
            name='ProjectTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип проекта',
                'verbose_name_plural': 'Типы проектов',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Разделы',
            },
        ),
        migrations.CreateModel(
            name='TaxAuthorities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4, verbose_name='Код')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Налоговый орган',
                'verbose_name_plural': 'Налоговые органы',
            },
        ),
        migrations.CreateModel(
            name='Themes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Название')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='theme_section', to='case.section', verbose_name='Раздел')),
            ],
            options={
                'verbose_name': 'Тема',
                'verbose_name_plural': 'Темы',
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.CharField(max_length=200, verbose_name='Сообщение')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='case.cases', verbose_name='Дело')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
    ]
