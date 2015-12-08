# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0012_auto_20151201_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_class',
            name='period',
            field=models.IntegerField(choices=tuple(zip(range(1, 8), (str(i) for i in range(1, 8))))),
        ),
    ]
