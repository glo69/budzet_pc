# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-27 20:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybudget', '0003_baza_wydatkow_okres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baza_wydatkow',
            name='nazwa',
        ),
    ]