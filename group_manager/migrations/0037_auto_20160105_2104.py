# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 21:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0036_auto_20160105_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=500, unique=True)),
                ('detail', models.TextField()),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
            },
        ),
        migrations.RemoveField(
            model_name='debate',
            name='debate_group',
        ),
        migrations.AddField(
            model_name='debate',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='group_manager.Student_Group'),
        ),
        migrations.AddField(
            model_name='student_group',
            name='position',
            field=models.NullBooleanField(choices=[(None, '---'), (True, 'Affirmative'), (False, 'Negative')]),
        ),
        migrations.AddField(
            model_name='schedule',
            name='Topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='group_manager.Topic'),
        ),
    ]