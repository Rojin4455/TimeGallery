# Generated by Django 5.0.1 on 2024-02-01 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterField(
            model_name='category',
            name='cat_slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
