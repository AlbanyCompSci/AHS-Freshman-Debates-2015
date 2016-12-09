# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0004_auto_20151103_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.ForeignKey(null=True, to='group_manager.Student_Group', on_delete=models.CASCADE),
        ),
    ]
