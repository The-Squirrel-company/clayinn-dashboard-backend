from django.db import migrations, models
from django.utils import timezone

def set_created_at(apps, schema_editor):
    Lead = apps.get_model('leads_management', 'Lead')
    Lead.objects.all().update(created_at=timezone.now())

class Migration(migrations.Migration):
    dependencies = [
        ('leads_management', '0002_lead_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now),
            preserve_default=False,
        ),
        migrations.RunPython(set_created_at),
    ] 