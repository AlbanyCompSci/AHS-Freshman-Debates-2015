# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0002_auto_20151102_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='type',
            field=models.IntegerField(choices=[(0, 'English'), (1, 'IHS')]),
        ),
    ]
