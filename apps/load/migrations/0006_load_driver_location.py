# Generated by Django 5.1.4 on 2025-04-15 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_load', '0005_driver_motive_id_alter_otherpay_pay_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='load',
            name='driver_location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
