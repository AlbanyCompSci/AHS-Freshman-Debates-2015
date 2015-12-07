# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import group_manager.fields


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0012_auto_20151201_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_class',
            name='period',
            field=group_manager.fields.IntegerRangeField(),
        ),
    ]
