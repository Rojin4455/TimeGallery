# Generated by Django 5.0.1 on 2024-01-25 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_account_is_superuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='firstname',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='account',
            name='lastname',
        ),
    ]