# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 05:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_auto_20171206_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='list',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='lists.List'),
        ),
    ]
