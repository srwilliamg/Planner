# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-18 15:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0012_auto_20170804_1759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datos_generales',
            name='departamento',
        ),
        migrations.RemoveField(
            model_name='datos_generales',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='datos_generales',
            name='vereda',
        ),
        migrations.AlterField(
            model_name='porcentaje_precio',
            name='porcentaje',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='porcentaje_precio',
            name='precio',
            field=models.FloatField(default=1),
        ),
    ]
