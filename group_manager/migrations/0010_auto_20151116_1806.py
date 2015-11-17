# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0009_auto_20151110_1917'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['english_class', 'last_name', 'first_name'], 'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
    ]
