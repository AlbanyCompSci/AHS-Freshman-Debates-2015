# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import group_manager.fields


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0013_auto_20151207_1850'),
    ]

    operations = [
        migrations.CreateModel(
            name='Debate',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('isPresenting', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Debates',
                'verbose_name': 'Debate',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('location', models.CharField(max_length=140, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Locations',
                'verbose_name': 'Location ',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('period', group_manager.fields.IntegerRangeField()),
                ('date', models.DateField()),
                ('location', models.ForeignKey(to='group_manager.Location')),
            ],
            options={
                'verbose_name_plural': 'Schedules',
                'verbose_name': 'Schedule',
            },
        ),
        migrations.RemoveField(
            model_name='debate_group',
            name='location',
        ),
        migrations.RemoveField(
            model_name='debate_group',
            name='time',
        ),
        migrations.AlterField(
            model_name='judge',
            name='student_id',
            field=models.BigIntegerField(unique=True, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.BigIntegerField(unique=True, serialize=False, primary_key=True),
        ),
        migrations.AlterUniqueTogether(
            name='student_class',
            unique_together=set([('teacher', 'period')]),
        ),
        migrations.AddField(
            model_name='debate',
            name='debate_group',
            field=models.ForeignKey(to='group_manager.Debate_Group'),
        ),
        migrations.AddField(
            model_name='debate',
            name='schedule',
            field=models.ForeignKey(to='group_manager.Schedule'),
        ),
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together=set([('period', 'location', 'date')]),
        ),
        migrations.AlterUniqueTogether(
            name='debate',
            unique_together=set([('schedule', 'isPresenting')]),
        ),
    ]
