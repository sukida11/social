# Generated by Django 4.1.1 on 2022-10-02 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_profilepost_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepost',
            name='pub_date',
            field=models.DateTimeField(null=True),
        ),
    ]
