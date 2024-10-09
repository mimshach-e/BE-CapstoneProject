# Generated by Django 5.1.1 on 2024-10-07 11:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('discount_type', models.CharField(choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')], default='percentage', max_length=15)),
                ('value', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(None)])),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateField()),
                ('active', models.BooleanField(default=True)),
                ('products', models.ManyToManyField(related_name='discounts', to='products.product')),
            ],
        ),
    ]
