# Generated by Django 4.2.4 on 2024-05-11 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='id_capital',
            new_name='is_capital',
        ),
    ]
