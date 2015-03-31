# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0002_auto_20150329_1751'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('rated_object', models.ForeignKey(to='src.RatedObject', null=True)),
                ('reviewer', models.ForeignKey(to='src.User', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('grade', models.DecimalField(max_digits=2, decimal_places=1)),
                ('attribute', models.ForeignKey(to='src.Attribute', null=True)),
                ('review', models.ForeignKey(to='src.Review', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='score',
        ),
    ]
