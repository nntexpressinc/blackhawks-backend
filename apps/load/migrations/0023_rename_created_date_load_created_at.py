# Generated by Django 5.2 on 2025-04-30 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps_load', '0022_rename_created_date_load_created_at_stops_location_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='load',
            old_name='created_date',
            new_name='created_at',
        ),
    ]
