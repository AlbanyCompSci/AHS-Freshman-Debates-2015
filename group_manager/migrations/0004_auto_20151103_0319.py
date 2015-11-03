# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0003_auto_20151103_0243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='judge',
            name='id',
        ),
        migrations.RemoveField(
            model_name='student',
            name='id',
        ),
        migrations.AlterField(
            model_name='judge',
            name='student_id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='student_group',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True),
        ),
    ]
