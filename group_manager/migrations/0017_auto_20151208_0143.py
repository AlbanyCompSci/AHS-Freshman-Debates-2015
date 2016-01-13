# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0016_auto_20151208_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debate',
            name='isPresenting',
            field=models.BooleanField(verbose_name='group presenting'),
        ),
    ]
