# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0014_auto_20151208_0002'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='debate_group',
            options={'verbose_name_plural': 'Debate Groups', 'verbose_name': 'Debate Group'},
        ),
    ]
