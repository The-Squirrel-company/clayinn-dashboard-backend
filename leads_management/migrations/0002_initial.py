# Generated by Django 5.1.2 on 2024-11-15 13:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookings_management', '0003_initial'),
        ('leads_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='sales_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='occasion',
            name='booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='occasions', to='bookings_management.booking'),
        ),
        migrations.AddField(
            model_name='occasion',
            name='lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='occasions', to='leads_management.lead'),
        ),
        migrations.AddField(
            model_name='postcallstatus',
            name='lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_call_statuses', to='leads_management.lead'),
        ),
        migrations.AddField(
            model_name='visit',
            name='lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='leads_management.lead'),
        ),
    ]