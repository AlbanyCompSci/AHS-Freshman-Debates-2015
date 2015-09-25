# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Debate_Group',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('time', models.DateTimeField()),
                ('location', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Debates',
                'verbose_name': 'Debate',
            },
        ),
        migrations.CreateModel(
            name='English_Class',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('period', models.IntegerField()),
                ('teacher', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'English Classes',
                'verbose_name': 'English Class',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('english_class', models.ForeignKey(to='group_manager.English_Class')),
            ],
            options={
                'verbose_name_plural': 'Students',
                'verbose_name': 'Student',
            },
        ),
        migrations.CreateModel(
            name='Student_Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('teacher', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Student Groups',
                'verbose_name': 'Student Group',
            },
        ),
        migrations.AddField(
            model_name='student',
            name='group',
            field=models.ForeignKey(to='group_manager.Student_Group'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='debate_group',
            name='affTeam',
            field=models.OneToOneField(to='group_manager.Student_Group', related_name='affTeam'),
        ),
        migrations.AddField(
            model_name='debate_group',
            name='judge',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='debate_group',
            name='negTeam',
            field=models.OneToOneField(to='group_manager.Student_Group', related_name='negTeam'),
        ),
    ]
