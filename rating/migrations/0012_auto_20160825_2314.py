# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-25 20:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0011_auto_20160825_2302'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='athlete_route',
            unique_together=set([]),
        ),
    ]
