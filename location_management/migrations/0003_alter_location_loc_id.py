# Generated by Django 5.1.2 on 2024-10-20 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location_management', '0002_remove_location_location_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='loc_id',
            field=models.CharField(editable=False, max_length=25, primary_key=True, serialize=False),
        ),
    ]