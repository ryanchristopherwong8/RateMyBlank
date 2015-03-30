# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
<<<<<<< HEAD
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=80)),
                ('password', models.CharField(max_length=10)),
=======
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('publish_date', models.DateField(max_length=200)),
>>>>>>> 5162367a2490819b909a80a35b48806bd273b04c
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
