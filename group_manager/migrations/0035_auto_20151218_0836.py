# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-18 08:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0034_auto_20151218_0339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='judge_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='group_manager.Judge_Group'),
        ),
    ]
