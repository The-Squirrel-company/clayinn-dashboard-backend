from django.db import models
from venue_management.models import Venue
from user_management.models import User
from location_management.models import Location

# Create your models here.

class Lead(models.Model):
    LEAD_STATUS_CHOICES = [
        ('untouched', 'Untouched'),
        ('proposal_sent', 'Proposal Sent'),
        ('visit_scheduled', 'Visit Scheduled'),
        ('visit_done', 'Visit Done'),
        ('final_negotiation', 'Final Negotiation'),
        ('postponed', 'Postponed'),
        ('confirmation_awaited', 'Confirmation Awaited'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
    ]

    CALL_STATUS_CHOICES = [
        ('not_yet_call', 'Not Yet Called'),
        ('call_later', 'Call Later'),
        ('language_problem', 'Language Problem'),
        ('busy', 'Busy'),
        ('failed', 'Failed'),
        ('disconnected', 'Disconnected'),
        ('not_connected', 'Not Connected'),
        ('abandoned', 'Abandoned'),
    ]

    lead_number = models.AutoField(primary_key=True)
    lead_entry_date = models.DateTimeField(auto_now_add=True)
    hostname = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    lead_status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='untouched')
    call_status = models.CharField(max_length=20, choices=CALL_STATUS_CHOICES, default='not_yet_call')
    followup = models.DateField(null=True, blank=True)
    remark = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    location = models.ForeignKey('location_management.Location', on_delete=models.CASCADE)
    sales_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leads')

class BaseOccasion(models.Model):
    YES_NO_NUMBER_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('number', 'Number'),
    ]
    
    date_of_function = models.DateField()
    day = models.CharField(max_length=10)
    
    lunch_min_pax_type = models.CharField(max_length=6, choices=YES_NO_NUMBER_CHOICES, default='no')
    lunch_min_pax_value = models.IntegerField(null=True, blank=True)
    
    hi_tea_min_pax_type = models.CharField(max_length=6, choices=YES_NO_NUMBER_CHOICES, default='no')
    hi_tea_min_pax_value = models.IntegerField(null=True, blank=True)
    
    dinner_min_pax_type = models.CharField(max_length=6, choices=YES_NO_NUMBER_CHOICES, default='no')
    dinner_min_pax_value = models.IntegerField(null=True, blank=True)
    
    dj_type = models.CharField(max_length=6, choices=YES_NO_NUMBER_CHOICES, default='no')
    dj_value = models.IntegerField(null=True, blank=True)
    
    decor_type = models.CharField(max_length=6, choices=YES_NO_NUMBER_CHOICES, default='no')
    decor_value = models.IntegerField(null=True, blank=True)
    
    liquor_type = models.CharField(max_length=6, choices=YES_NO_NUMBER_CHOICES, default='no')
    liquor_value = models.IntegerField(null=True, blank=True)
    
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True

class StandardOccasion(BaseOccasion):
    class Meta:
        abstract = True

class Engagement(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='engagements')

class Sagan(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='sagans')

class Roka(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='rokas')

class Haldi(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='haldis')

class Mehndi(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='mehndis')

class Wedding(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='weddings')
    vedi_type = models.CharField(max_length=6, choices=BaseOccasion.YES_NO_NUMBER_CHOICES, default='no')
    vedi_value = models.IntegerField(null=True, blank=True)

class Reception(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='receptions')

class Rooms(BaseOccasion):
    number_of_pax = models.IntegerField()
    number_of_rooms = models.IntegerField()
    plan = models.CharField(max_length=255)

class Corporate(StandardOccasion):
    vedi_type = models.CharField(max_length=6, choices=BaseOccasion.YES_NO_NUMBER_CHOICES, default='no')
    vedi_value = models.IntegerField(null=True, blank=True)

class Visit(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='visits')
    date = models.DateField()
    time = models.TimeField()
    text = models.TextField()

class PostCallStatus(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='post_call_statuses')
    date = models.DateField()
    time = models.TimeField()
    text = models.TextField()
