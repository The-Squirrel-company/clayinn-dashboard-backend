# Generated by Django 5.1.2 on 2024-11-15 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Occasion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occasion_type', models.CharField(choices=[('engagement', 'Engagement'), ('wedding', 'Wedding'), ('reception', 'Reception'), ('sagan', 'Sagan'), ('roka', 'Roka'), ('haldi', 'Haldi'), ('mehndi', 'Mehndi'), ('corporate', 'Corporate'), ('room', 'Room')], max_length=20)),
                ('date_of_function', models.DateField(blank=True, null=True)),
                ('day', models.CharField(blank=True, max_length=10)),
                ('lunch_pax', models.IntegerField(default=0)),
                ('hi_tea_pax', models.IntegerField(default=0)),
                ('dinner_pax', models.IntegerField(default=0)),
                ('dj_value', models.IntegerField(default=0)),
                ('decor_value', models.IntegerField(default=0)),
                ('liquor_value', models.IntegerField(default=0)),
                ('vedi_value', models.IntegerField(default=0)),
                ('number_of_pax', models.IntegerField(default=0)),
                ('number_of_rooms', models.IntegerField(default=0)),
                ('plan', models.CharField(blank=True, max_length=255)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'ordering': ['date_of_function'],
            },
        ),
        migrations.CreateModel(
            name='PostCallStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('lead_number', models.AutoField(primary_key=True, serialize=False)),
                ('lead_entry_date', models.DateTimeField(auto_now_add=True)),
                ('hostname', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=15)),
                ('lead_status', models.CharField(choices=[('untouched', 'Untouched'), ('proposal_sent', 'Proposal Sent'), ('visit_scheduled', 'Visit Scheduled'), ('visit_done', 'Visit Done'), ('final_negotiation', 'Final Negotiation'), ('postponed', 'Postponed'), ('confirmation_awaited', 'Confirmation Awaited'), ('closed_won', 'Closed Won'), ('closed_lost', 'Closed Lost')], default='untouched', max_length=20)),
                ('call_status', models.CharField(choices=[('not_yet_call', 'Not Yet Called'), ('call_later', 'Call Later'), ('language_problem', 'Language Problem'), ('busy', 'Busy'), ('failed', 'Failed'), ('disconnected', 'Disconnected'), ('not_connected', 'Not Connected'), ('abandoned', 'Abandoned')], default='not_yet_call', max_length=20)),
                ('followup', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='location_management.location')),
            ],
        ),
    ]
