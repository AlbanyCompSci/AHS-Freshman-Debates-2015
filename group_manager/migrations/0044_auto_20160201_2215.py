# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-01 22:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0043_auto_20160111_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debate',
            name='isPresenting',
            field=models.BooleanField(verbose_name='group presenting?'),
        ),
    ]