# Generated by Django 4.2.7 on 2024-02-20 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_additional_product_image_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute_value',
            name='attribute',
        ),
        migrations.DeleteModel(
            name='Attribute',
        ),
    ]
