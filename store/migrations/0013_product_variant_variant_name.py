# Generated by Django 4.2.7 on 2024-02-22 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_product_variant_thumbnail_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_variant',
            name='variant_name',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
