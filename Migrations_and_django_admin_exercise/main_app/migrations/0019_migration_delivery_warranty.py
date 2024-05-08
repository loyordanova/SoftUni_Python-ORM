# Generated by Django 4.2.4 on 2024-05-08 14:05

from django.db import migrations
from django.utils import timezone

def update_delivery_warranty(apps, schema_editor):
    order_model = apps.get_model('main_app', 'Order')

    orders = order_model.objects.all()

    for order in orders:
        if order.status == 'Pending':
            order.delivery = order.order_date + timezone.timedelta(days=3)
            order.save()
        elif order.status == 'Completed':
            order.warranty = '24 months'
            order.save()
        elif order.status == 'Canceled':
            order.delete()

def reverse_delivery_and_warranty(apps, schema_editor):
    order_model = apps.get_model('main_app', 'Order')

    orders = order_model.objects.all()

    delivery_default = order_model._meta.get_field('delivery').default

    warranty_default = order_model._meta.get_field('warranty').default

    for order in orders:
        if order.status == 'Pending':
            order.delivery = delivery_default
            order.save()
        elif order.status == 'Completed':
            order.warranty = warranty_default
            order.save()

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0018_order'),
    ]

    operations = [
    ]