# Generated by Django 4.2.4 on 2024-05-07 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_product_created_on_product_last_edited'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
