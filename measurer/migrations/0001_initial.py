# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-30 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_name', models.CharField(max_length=50)),
                ('material_density', models.FloatField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
