from django.db import models
from venue_management.models import Venue
from location_management.models import Location
from user_management.models import User

class Booking(models.Model):
    SLOT_CHOICES = [
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]

    OCCASION_CHOICES = [
        ('engagement', 'Engagement'),
        ('wedding', 'Wedding'),
        ('corporate', 'Corporate'),
        ('sagan', 'Sagan'),
        ('roka', 'Roka'),
        ('haldi', 'Haldi'),
        ('mehndi', 'Mehndi'),
        ('reception', 'Reception'),
    ]

    booking_number = models.AutoField(primary_key=True)
    lead = models.ForeignKey('leads_management.Lead', on_delete=models.PROTECT, related_name='bookings')
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    sales_person = models.ForeignKey(User, on_delete=models.PROTECT)
    
    # Booking Details
    booking_date = models.DateTimeField(auto_now_add=True)
    event_date = models.DateField()
    slot = models.CharField(max_length=10, choices=SLOT_CHOICES)
    
    # Occasion Details (with defaults)
    occasion_type = models.CharField(
        max_length=20, 
        choices=OCCASION_CHOICES,
        default='wedding'  # Adding a default value
    )
    occasion_id = models.IntegerField(default=0)  # Adding a default value

    class Meta:
        ordering = ['-booking_date']
        unique_together = ['venue', 'event_date', 'slot']

    def __str__(self):
        return f"Booking #{self.booking_number}"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Validate that the occasion_id exists in the corresponding occasion table
        if self.occasion_type and self.occasion_id:
            model_map = {
                'engagement': 'leads_management.Engagement',
                'wedding': 'leads_management.Wedding',
                'corporate': 'leads_management.Corporate',
                'sagan': 'leads_management.Sagan',
                'roka': 'leads_management.Roka',
                'haldi': 'leads_management.Haldi',
                'mehndi': 'leads_management.Mehndi',
                'reception': 'leads_management.Reception',
            }
            
            from django.apps import apps
            model = apps.get_model(model_map[self.occasion_type])
            if not model.objects.filter(id=self.occasion_id, lead=self.lead).exists():
                raise ValidationError(f'Invalid occasion_id for the specified occasion_type and lead')