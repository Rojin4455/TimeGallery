# Generated by Django 5.0.1 on 2024-01-25 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0004_account_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Account',
        ),
    ]
