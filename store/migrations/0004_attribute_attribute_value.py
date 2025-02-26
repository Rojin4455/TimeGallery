# Generated by Django 4.2.7 on 2024-02-19 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_product_price_remove_product_stock_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_name', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Attribute_Value',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_value', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.attribute')),
            ],
        ),
    ]
