# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-22 19:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0003_base_presupuestal_establecimiento'),
    ]

    operations = [
        migrations.RenameField(
            model_name='base_presupuestal',
            old_name='establecimiento',
            new_name='establecimiento_r',
        ),
    ]