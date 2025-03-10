from django.db import models
from user_management.models import User
from location_management.models import Location

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

    LEAD_SOURCE_CHOICES = [
        ('walk_in', 'Walk In'),
        ('social_media', 'Social Media'),
        ('google', 'Google'),
        ('referral', 'Referral'),
        ('wedding_wire', 'Wedding Wire'),
        ('wed_me_good', 'Wed Me Good'),
        ('venue_look', 'Venue Look'),
        ('venue_monk', 'Venue Monk'),
        ('sloshout', 'Sloshout'),
        ('others', 'Others'),
    ]

    lead_number = models.AutoField(primary_key=True)
    lead_entry_date = models.DateTimeField(auto_now_add=True)
    hostname = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    lead_status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='untouched')
    call_status = models.CharField(max_length=20, choices=CALL_STATUS_CHOICES, default='not_yet_call')
    followup = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='leads')
    sales_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leads')
    remark = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lead_source = models.CharField(
        max_length=20, 
        choices=LEAD_SOURCE_CHOICES, 
        default='others'
    )

class Occasion(models.Model):
    OCCASION_TYPES = [
        ('engagement', 'Engagement'),
        ('wedding', 'Wedding'),
        ('reception', 'Reception'),
        ('sagan', 'Sagan'),
        ('roka', 'Roka'),
        ('haldi', 'Haldi'),
        ('mehndi', 'Mehndi'),
        ('corporate', 'Corporate'),
        ('room', 'Room')
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='occasions')
    occasion_type = models.CharField(max_length=20, choices=OCCASION_TYPES)
    date_of_function = models.DateField()
    day = models.CharField(max_length=10, blank=True)
    
    # Fields for regular occasions
    lunch_pax = models.IntegerField(default=0)
    hi_tea_pax = models.IntegerField(default=0)
    dinner_pax = models.IntegerField(default=0)
    dj_value = models.IntegerField(default=0)
    decor_value = models.IntegerField(default=0)
    liquor_value = models.IntegerField(default=0)
    vedi_value = models.IntegerField(default=0)
    
    # Fields for room bookings
    number_of_pax = models.IntegerField(default=0)
    number_of_rooms = models.IntegerField(default=0)
    plan = models.CharField(max_length=255, blank=True)
    
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['date_of_function']

class Visit(models.Model):
    lead = models.ForeignKey('Lead', on_delete=models.CASCADE, related_name='visits')
    date = models.DateField()
    time = models.TimeField()
    text = models.TextField()

class PostCallStatus(models.Model):
    lead = models.ForeignKey('Lead', on_delete=models.CASCADE, related_name='post_call_statuses')
    date = models.DateField()
    time = models.TimeField()
    text = models.TextField()
