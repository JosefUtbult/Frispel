# Generated by Django 3.2.7 on 2021-09-21 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0015_auto_20210921_1734'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='expiry_date',
            new_name='application_expiry_date',
        ),
    ]