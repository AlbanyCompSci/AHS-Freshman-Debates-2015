# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-29 01:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grading', '0002_auto_20160211_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoring_sheet',
            name='judge',
            field=models.CharField(max_length=140),
        ),
    ]
