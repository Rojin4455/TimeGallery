# Generated by Django 5.0.1 on 2024-03-17 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_grandtotal',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
    ]
