# Generated by Django 4.1.1 on 2022-10-02 14:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_profilepost_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepost',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 2, 14, 32, 39, 508635, tzinfo=datetime.timezone.utc)),
        ),
    ]