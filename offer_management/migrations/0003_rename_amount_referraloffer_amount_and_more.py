# Generated by Django 5.0.1 on 2024-03-18 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer_management', '0002_referraloffer_limit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='referraloffer',
            old_name='Amount',
            new_name='amount',
        ),
        migrations.AlterField(
            model_name='referraluser',
            name='code',
            field=models.CharField(max_length=8, null=True, unique=True),
        ),
    ]
