# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group_manager', '0006_auto_20151103_1814'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.IntegerField()),
                ('type', models.IntegerField(choices=[(0, 'English'), (1, 'IHS')])),
                ('teacher', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Classes',
                'verbose_name': 'Class',
            },
        ),
        migrations.RemoveField(
            model_name='class',
            name='teacher',
        ),
        migrations.AlterField(
            model_name='student',
            name='english_class',
            field=models.ForeignKey(related_name='english_class', to='group_manager.Student_Class'),
        ),
        migrations.AlterField(
            model_name='student',
            name='ihs_class',
            field=models.ForeignKey(to='group_manager.Student_Class'),
        ),
        migrations.DeleteModel(
            name='Class',
        ),
    ]
