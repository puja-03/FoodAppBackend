# Generated by Django 5.1.3 on 2025-04-08 17:21

import django.db.models.deletion
import kitchen.models
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
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kitchen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=10)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='kitchens/logos/')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='kitchens/covers/')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=255)),
                ('gst_number', models.CharField(max_length=50, unique=True)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=10)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profiles/')),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=255)),
                ('account_holder_name', models.CharField(max_length=255)),
                ('account_number', models.CharField(max_length=50, unique=True, validators=[kitchen.models.validate_account_number])),
                ('ifsc_code', models.CharField(max_length=20)),
                ('upi_id', models.CharField(blank=True, max_length=100, null=True)),
                ('kitchen', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='kitchen.kitchen')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=200)),
                ('Isavailable', models.BooleanField()),
                ('prep_Time', models.TimeField()),
                ('description', models.CharField(max_length=200)),
                ('Image', models.ImageField(blank=True, null=True, upload_to='kitchens/Images/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchen.category')),
                ('kitchen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchen.kitchen')),
            ],
        ),
        migrations.CreateModel(
            name='MenuQuantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('quantity_type', models.CharField(max_length=200)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quantities', to='kitchen.menu')),
            ],
        ),
    ]
