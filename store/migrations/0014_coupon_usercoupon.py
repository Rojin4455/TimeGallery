# Generated by Django 5.0.1 on 2024-03-08 15:20

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_product_variant_variant_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=100)),
                ('is_expired', models.BooleanField(default=False)),
                ('discount_percentage', models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('minimum_amount', models.IntegerField(default=400)),
                ('max_uses', models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('expire_date', models.DateField()),
                ('total_coupons', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='UserCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage_count', models.IntegerField(default=0)),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.coupon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
