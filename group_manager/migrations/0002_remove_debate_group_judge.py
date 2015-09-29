# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='debate_group',
            name='judge',
        ),
    ]
