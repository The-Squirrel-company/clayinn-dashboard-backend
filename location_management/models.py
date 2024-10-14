import uuid
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

def generate_location_id():
    return f"loc-{uuid.uuid4().hex[:5]}"

class Location(models.Model):
    loc_id = models.CharField(max_length=20, primary_key=True, default=generate_location_id, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.loc_id})"

@receiver(pre_delete, sender=Location)
def delete_related_data(sender, instance, **kwargs):
    # Delete related venues
    instance.venues.all().delete()
    
    # Delete related users
    instance.users.all().delete()
