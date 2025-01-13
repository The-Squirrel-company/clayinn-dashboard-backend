from django.db import models
from venue_management.models import Venue
from location_management.models import Location
from user_management.models import User
from leads_management.models import Lead, Occasion
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone

class Booking(models.Model):
    SLOT_CHOICES = [
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]

    booking_number = models.AutoField(primary_key=True)
    lead = models.ForeignKey(
        Lead, 
        on_delete=models.PROTECT, 
        related_name='bookings'
    )
    occasion = models.ForeignKey(
        Occasion,
        on_delete=models.PROTECT,
        related_name='bookings'
    )
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    sales_person = models.ForeignKey(User, on_delete=models.PROTECT)
    
    booking_date = models.DateTimeField(auto_now_add=True)
    event_date = models.DateField(null=False, blank=False)
    slot = models.CharField(max_length=10, choices=SLOT_CHOICES)

    class Meta:
        ordering = ['-booking_date']
        unique_together = ['venue', 'event_date', 'slot']

    def __str__(self):
        return f"Booking #{self.booking_number} - {self.event_date} ({self.slot})"

    def save(self, *args, **kwargs):
        if not self.location_id:
            self.location = self.venue.location
        if self.event_date:
            self.day = self.event_date.strftime('%A').lower()
        super().save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError
        # Check if venue is already booked for this date and slot
        if Booking.objects.filter(
            venue=self.venue,
            event_date=self.event_date,
            slot=self.slot
        ).exclude(booking_number=self.booking_number).exists():
            raise ValidationError('This venue is already booked for the specified date and slot')

@receiver(post_delete, sender=Booking)
def update_lead_status_after_booking_delete(sender, instance, **kwargs):
    lead = instance.lead
    # Check if lead has any remaining bookings
    if not lead.bookings.exists():
        lead.lead_status = 'untouched'
        lead.save()