# Generated by Django 5.0.1 on 2024-02-01 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=50, unique=True)),
                ('cat_slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('cat_image', models.ImageField(blank=True, upload_to='photos/cat_image')),
                ('cat_description', models.TextField(blank=True, max_length=255)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
