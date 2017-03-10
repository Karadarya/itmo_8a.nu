# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-10 21:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0017_auto_20170208_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athlete_info',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_picture/', verbose_name='\u0444\u043e\u0442\u043e'),
        ),
        migrations.AlterField(
            model_name='athlete_info',
            name='score',
            field=models.FloatField(null=True, verbose_name='\u0431\u0430\u043b\u043b\u044b'),
        ),
    ]