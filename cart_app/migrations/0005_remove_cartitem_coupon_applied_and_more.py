# Generated by Django 5.0.1 on 2024-03-20 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart_app', '0004_cartitem_coupon_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='coupon_applied',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='coupon_discount',
        ),
    ]