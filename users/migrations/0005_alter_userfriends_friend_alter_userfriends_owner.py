# Generated by Django 4.1.1 on 2022-10-01 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_user2_userfriends_friend_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfriends',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userfriends',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]