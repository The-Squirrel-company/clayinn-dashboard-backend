# Generated by Django 5.1.2 on 2024-10-20 08:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location_management', '0003_alter_location_loc_id'),
        ('venue_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Corporate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_function', models.DateField()),
                ('day', models.CharField(max_length=10)),
                ('lunch_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('lunch_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('hi_tea_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('hi_tea_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dinner_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dinner_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dj_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dj_value', models.IntegerField(blank=True, null=True)),
                ('decor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('decor_value', models.IntegerField(blank=True, null=True)),
                ('liquor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('liquor_value', models.IntegerField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('vedi_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('vedi_value', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_function', models.DateField()),
                ('day', models.CharField(max_length=10)),
                ('lunch_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('lunch_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('hi_tea_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('hi_tea_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dinner_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dinner_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dj_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dj_value', models.IntegerField(blank=True, null=True)),
                ('decor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('decor_value', models.IntegerField(blank=True, null=True)),
                ('liquor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('liquor_value', models.IntegerField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('number_of_pax', models.IntegerField()),
                ('number_of_rooms', models.IntegerField()),
                ('plan', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
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
                ('remark', models.TextField(blank=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='location_management.location')),
                ('sales_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venue_management.venue')),
            ],
        ),
        migrations.CreateModel(
            name='Haldi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_function', models.DateField()),
                ('day', models.CharField(max_length=10)),
                ('lunch_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('lunch_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('hi_tea_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('hi_tea_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dinner_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dinner_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dj_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dj_value', models.IntegerField(blank=True, null=True)),
                ('decor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('decor_value', models.IntegerField(blank=True, null=True)),
                ('liquor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('liquor_value', models.IntegerField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='haldis', to='leads_management.lead')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Engagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_function', models.DateField()),
                ('day', models.CharField(max_length=10)),
                ('lunch_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('lunch_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('hi_tea_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('hi_tea_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dinner_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dinner_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dj_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dj_value', models.IntegerField(blank=True, null=True)),
                ('decor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('decor_value', models.IntegerField(blank=True, null=True)),
                ('liquor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('liquor_value', models.IntegerField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engagements', to='leads_management.lead')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Mehndi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_function', models.DateField()),
                ('day', models.CharField(max_length=10)),
                ('lunch_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('lunch_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('hi_tea_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('hi_tea_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dinner_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dinner_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dj_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dj_value', models.IntegerField(blank=True, null=True)),
                ('decor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('decor_value', models.IntegerField(blank=True, null=True)),
                ('liquor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('liquor_value', models.IntegerField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mehndis', to='leads_management.lead')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PostCallStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('text', models.TextField()),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_call_statuses', to='leads_management.lead')),
            ],
        ),
        migrations.CreateModel(
            name='Reception',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_function', models.DateField()),
                ('day', models.CharField(max_length=10)),
                ('lunch_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('lunch_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('hi_tea_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('hi_tea_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dinner_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dinner_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dj_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dj_value', models.IntegerField(blank=True, null=True)),
                ('decor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('decor_value', models.IntegerField(blank=True, null=True)),
                ('liquor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('liquor_value', models.IntegerField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receptions', to='leads_management.lead')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Roka',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_function', models.DateField()),
                ('day', models.CharField(max_length=10)),
                ('lunch_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('lunch_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('hi_tea_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('hi_tea_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dinner_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dinner_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dj_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dj_value', models.IntegerField(blank=True, null=True)),
                ('decor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('decor_value', models.IntegerField(blank=True, null=True)),
                ('liquor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('liquor_value', models.IntegerField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rokas', to='leads_management.lead')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sagan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_function', models.DateField()),
                ('day', models.CharField(max_length=10)),
                ('lunch_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('lunch_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('hi_tea_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('hi_tea_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dinner_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dinner_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dj_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dj_value', models.IntegerField(blank=True, null=True)),
                ('decor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('decor_value', models.IntegerField(blank=True, null=True)),
                ('liquor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('liquor_value', models.IntegerField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sagans', to='leads_management.lead')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('text', models.TextField()),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='leads_management.lead')),
            ],
        ),
        migrations.CreateModel(
            name='Wedding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_function', models.DateField()),
                ('day', models.CharField(max_length=10)),
                ('lunch_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('lunch_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('hi_tea_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('hi_tea_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dinner_min_pax_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dinner_min_pax_value', models.IntegerField(blank=True, null=True)),
                ('dj_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('dj_value', models.IntegerField(blank=True, null=True)),
                ('decor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('decor_value', models.IntegerField(blank=True, null=True)),
                ('liquor_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('liquor_value', models.IntegerField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('vedi_type', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no', max_length=6)),
                ('vedi_value', models.IntegerField(blank=True, null=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weddings', to='leads_management.lead')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
