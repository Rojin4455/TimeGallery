# Generated by Django 5.0.1 on 2024-03-18 11:00

from django.db import migrations,models

def copy_sale_price_to_offer_price(apps, schema_editor):
    Product_Variant = apps.get_model('store', 'Product_Variant')

    # Update offer_price with sale_price for existing instances
    for variant in Product_Variant.objects.all():
        variant.offer_price = variant.sale_price
        variant.save()


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_product_variant_offer_product_variant_offer_discount'),
    ]

    operations = [
        migrations.RunPython(copy_sale_price_to_offer_price),

    ]