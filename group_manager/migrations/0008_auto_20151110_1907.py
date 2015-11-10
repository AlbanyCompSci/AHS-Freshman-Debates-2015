# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0007_auto_20151108_0015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name_plural': 'Students', 'ordering': ['last_name', 'first_name'], 'verbose_name': 'Student'},
        ),
    ]
