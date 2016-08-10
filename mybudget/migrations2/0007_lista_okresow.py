# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-13 19:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mybudget', '0006_typ_wydatku_nazwa_skrocona'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lista_okresow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa_okresu', models.CharField(max_length=8)),
                ('wplywy_w_okresie', models.DecimalField(decimal_places=2, max_digits=9)),
                ('komentarz', models.CharField(max_length=256)),
                ('ilosc_dni', models.IntegerField()),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]