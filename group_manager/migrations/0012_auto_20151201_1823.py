# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0011_auto_20151127_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.ForeignKey(blank=True, to='group_manager.Student_Group', on_delete=django.db.models.deletion.SET_NULL, null=True),
        ),
    ]
