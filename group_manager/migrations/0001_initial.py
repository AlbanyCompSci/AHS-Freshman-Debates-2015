# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('period', models.IntegerField()),
                ('type', models.IntegerField(choices=[(1, 'English'), (2, 'IHS')])),
                ('teacher', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Class',
                'verbose_name_plural': 'Classes',
            },
        ),
        migrations.CreateModel(
            name='Debate_Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=140)),
                ('time', models.DateTimeField()),
                ('location', models.CharField(max_length=140)),
            ],
            options={
                'verbose_name': 'Debate',
                'verbose_name_plural': 'Debates',
            },
        ),
        migrations.CreateModel(
            name='Judge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('student_id', models.BigIntegerField()),
                ('first_name', models.CharField(max_length=140)),
                ('last_name', models.CharField(max_length=140)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('student_id', models.BigIntegerField()),
                ('first_name', models.CharField(max_length=140)),
                ('last_name', models.CharField(max_length=140)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('english_class', models.ForeignKey(related_name='english_class', to='group_manager.Class', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='Student_Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('teacher', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Student Group',
                'verbose_name_plural': 'Student Groups',
            },
        ),
        migrations.AddField(
            model_name='student',
            name='group',
            field=models.ForeignKey(to='group_manager.Student_Group', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='student',
            name='ihs_class',
            field=models.ForeignKey(to='group_manager.Class', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='debate_group',
            name='affTeam',
            field=models.OneToOneField(related_name='affTeam', to='group_manager.Student_Group', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='debate_group',
            name='judge',
            field=models.ManyToManyField(to='group_manager.Judge'),
        ),
        migrations.AddField(
            model_name='debate_group',
            name='negTeam',
            field=models.OneToOneField(related_name='negTeam', to='group_manager.Student_Group', on_delete=models.CASCADE),
        ),
    ]
