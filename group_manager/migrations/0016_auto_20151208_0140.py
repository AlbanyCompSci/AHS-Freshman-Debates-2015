# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0015_auto_20151208_0008'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='debate',
            unique_together=set([('schedule', 'isPresenting'), ('debate_group', 'schedule')]),
        ),
    ]
