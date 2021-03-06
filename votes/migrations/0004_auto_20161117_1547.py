# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-17 14:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0003_choice_votes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(editable=False, max_length=6)),
                ('used', models.BooleanField(default=False, editable=False)),
            ],
        ),
        migrations.AlterField(
            model_name='choice',
            name='votes',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
