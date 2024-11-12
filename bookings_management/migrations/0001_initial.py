# Generated by Django 5.1.2 on 2024-11-04 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_number', models.AutoField(primary_key=True, serialize=False)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('event_date', models.DateField()),
                ('slot', models.CharField(choices=[('afternoon', 'Afternoon'), ('evening', 'Evening')], max_length=10)),
                ('occasion_type', models.CharField(choices=[('engagement', 'Engagement'), ('wedding', 'Wedding'), ('corporate', 'Corporate'), ('sagan', 'Sagan'), ('roka', 'Roka'), ('haldi', 'Haldi'), ('mehndi', 'Mehndi'), ('reception', 'Reception')], default='wedding', max_length=20)),
                ('occasion_id', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-booking_date'],
            },
        ),
    ]