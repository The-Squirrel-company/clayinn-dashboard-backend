# Generated by Django 5.1.2 on 2024-11-15 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('loc_id', models.CharField(editable=False, max_length=25, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
            ],
        ),
    ]
