# Generated by Django 5.1.2 on 2024-11-15 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0026_historicalstockrequest_cutoff_datetime_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalstock",
            old_name="at_location",
            new_name="transferred",
        ),
        migrations.RenameField(
            model_name="stock",
            old_name="at_location",
            new_name="transferred",
        ),
    ]
