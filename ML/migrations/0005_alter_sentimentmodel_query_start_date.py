# Generated by Django 4.2.5 on 2024-01-25 22:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ML', '0004_alter_sentimentmodel_query_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentimentmodel',
            name='query_start_date',
            field=models.DateField(default=datetime.date(2023, 1, 25)),
        ),
    ]
