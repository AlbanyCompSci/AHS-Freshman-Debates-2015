# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-18 03:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0033_auto_20151217_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debate_group',
            name='title',
            field=models.CharField(max_length=140, verbose_name='topic'),
        ),
    ]