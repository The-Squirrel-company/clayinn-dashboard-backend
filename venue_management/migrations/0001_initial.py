# Generated by Django 5.1.2 on 2024-10-14 09:38

import django.db.models.deletion
import venue_management.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('venue_id', models.CharField(default=venue_management.models.generate_venue_id, editable=False, max_length=25, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='venues', to='location_management.location')),
            ],
        ),
    ]
