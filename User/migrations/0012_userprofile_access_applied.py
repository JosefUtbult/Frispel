# Generated by Django 3.2.7 on 2021-09-21 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0011_userprofile_trubadur_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='access_applied',
            field=models.BooleanField(default=False),
        ),
    ]