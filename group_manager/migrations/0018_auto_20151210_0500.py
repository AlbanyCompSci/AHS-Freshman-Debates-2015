# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-10 05:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group_manager', '0017_auto_20151208_0143'),
    ]

    operations = [
        migrations.CreateModel(
            name='Judge_Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Judge Group',
                'verbose_name_plural': 'Judge Groups',
            },
        ),
        migrations.RemoveField(
            model_name='debate_group',
            name='judge',
        ),
        migrations.AddField(
            model_name='debate',
            name='judge_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='group_manager.Judge_Group'),
        ),
        migrations.AddField(
            model_name='judge',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='group_manager.Judge_Group'),
        ),
    ]