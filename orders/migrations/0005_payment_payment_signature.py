# Generated by Django 5.0.1 on 2024-03-08 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_orderproduct_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_signature',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
