# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-16 04:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0029_auto_20151215_2151'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='debate',
            unique_together=set([('debate_group', 'schedule')]),
        ),
    ]
