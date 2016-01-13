# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0008_auto_20151110_1907'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='judge',
            options={'verbose_name': 'Judge', 'verbose_name_plural': 'Judges', 'ordering': ['last_name', 'first_name']},
        ),
        migrations.AlterModelOptions(
            name='student_class',
            options={'verbose_name': 'Class', 'verbose_name_plural': 'Classes', 'ordering': ['teacher', 'period']},
        ),
    ]
