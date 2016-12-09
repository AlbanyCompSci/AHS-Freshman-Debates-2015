# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0010_auto_20151116_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='english_class',
            field=models.ForeignKey(to='group_manager.Student_Class', blank=True, related_name='english_class', null=True, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='student',
            name='ihs_class',
            field=models.ForeignKey(to='group_manager.Student_Class', blank=True, null=True, on_delete=models.CASCADE),
        ),
    ]
