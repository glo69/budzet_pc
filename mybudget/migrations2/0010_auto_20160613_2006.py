# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-13 20:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mybudget', '0009_auto_20160613_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lista_okresow',
            name='koniec_okresu',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lista_okresow',
            name='poczatek_okresu',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
