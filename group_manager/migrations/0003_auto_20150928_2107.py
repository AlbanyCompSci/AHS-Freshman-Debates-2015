# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group_manager', '0002_remove_debate_group_judge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='english_class',
            options={'verbose_name_plural': 'English Classses', 'verbose_name': 'English Class'},
        ),
        migrations.AddField(
            model_name='debate_group',
            name='judge',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='debate_group',
            name='location',
            field=models.CharField(max_length=140),
        ),
        migrations.AlterField(
            model_name='debate_group',
            name='title',
            field=models.CharField(max_length=140),
        ),
    ]
