# Generated by Django 5.0.1 on 2024-03-25 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='banner_caption',
            field=models.CharField(max_length=150, null=True),
        ),
    ]