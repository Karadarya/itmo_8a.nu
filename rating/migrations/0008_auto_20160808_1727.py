# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-08 14:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0007_auto_20160807_2312'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grade',
            options={'ordering': ['grade'], 'verbose_name': '\u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', 'verbose_name_plural': '\u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f'},
        ),
        migrations.AlterField(
            model_name='athlete_route',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0434\u0430\u0442\u0430'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='grade',
            field=models.CharField(max_length=50, verbose_name='\u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='route',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u043f\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u0430'),
        ),
    ]
