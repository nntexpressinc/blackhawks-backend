# Generated by Django 5.2 on 2025-04-26 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_load', '0016_alter_unit_dispatcher_alter_unit_driver_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='load',
            name='stop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_loads', to='apps_load.stops'),
        ),
    ]
