import uuid
from django.db import models
from location_management.models import Location

def generate_venue_id():
    return f"venue-{uuid.uuid4().hex[:5]}"

class Venue(models.Model):
    venue_id = models.CharField(max_length=25, primary_key=True, default=generate_venue_id, editable=False)
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='venues')

    def __str__(self):
        return f"{self.name} ({self.venue_id}) - {self.location.name}"
