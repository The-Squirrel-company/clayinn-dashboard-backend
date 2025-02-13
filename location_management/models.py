import uuid
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

def generate_location_id(name):
    # Clean the name to create a valid loc_id
    cleaned_name = ''.join(e for e in name if e.isalnum())  # Remove non-alphanumeric characters
    unique_suffix = uuid.uuid4().hex[:5]  # Generate a unique suffix
    return f"{cleaned_name}-{unique_suffix}"  # Combine name and unique suffix

class Location(models.Model):
    loc_id = models.CharField(max_length=100, primary_key=True, editable=False) 
    name = models.CharField(max_length=510) 
    address = models.TextField()

    def save(self, *args, **kwargs):
        if not self.loc_id:  # Only generate loc_id if it hasn't been set
            self.loc_id = generate_location_id(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.loc_id})"

    def delete(self, *args, **kwargs):
        # Delete all related bookings first
        from bookings_management.models import Booking
        Booking.objects.filter(location=self).delete()
        
        # Delete all related leads
        from leads_management.models import Lead
        Lead.objects.filter(location_id=self).delete()
        
        # Delete all venues
        self.venues.all().delete()
        
        # Delete all users
        self.users.all().delete()
        
        # Finally delete the location
        super().delete(*args, **kwargs)

@receiver(pre_delete, sender=Location)
def delete_related_data(sender, instance, **kwargs):
    # Delete related venues
    instance.venues.all().delete()
    
    # Delete related users
    instance.users.all().delete()
