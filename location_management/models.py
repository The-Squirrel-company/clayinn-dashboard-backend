import uuid
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from user_management.models import User

def generate_location_id():
    return f"loc-{uuid.uuid4().hex[:5]}"

class Location(models.Model):
    loc_id = models.CharField(max_length=20, primary_key=True, default=generate_location_id, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()
    location_admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_locations')

    def __str__(self):
        return f"{self.name} ({self.loc_id})"

    def delete(self, *args, **kwargs):
        # Store the associated admin user
        admin_user = self.location_admin
        
        # Set location_admin to None to avoid circular deletion
        self.location_admin = None
        self.save()
        
        # Delete the location
        super().delete(*args, **kwargs)
        
        # If there was an associated admin user, delete it
        if admin_user:
            try:
                admin_user.delete()
            except Exception as e:
                print(f"Error deleting admin user: {str(e)}")

@receiver(pre_delete, sender=Location)
def delete_location_admin(sender, instance, **kwargs):
    if instance.location_admin:
        admin_user = instance.location_admin
        instance.location_admin = None
        instance.save()
        try:
            admin_user.delete()
        except Exception as e:
            print(f"Error deleting admin user in signal: {str(e)}")
