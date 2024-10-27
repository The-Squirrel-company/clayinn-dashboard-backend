from django.db import models
from venue_management.models import Venue
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

    lead_number = models.AutoField(primary_key=True)
    lead_entry_date = models.DateTimeField(auto_now_add=True)
    hostname = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='leads')  # ForeignKey to Venue
    lead_status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='untouched')
    call_status = models.CharField(max_length=20, choices=CALL_STATUS_CHOICES, default='not_yet_call')
    followup = models.DateField(null=True, blank=True)
    remark = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='leads')  # ForeignKey to Location
    sales_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leads')

class StandardOccasion(models.Model):
    class Meta:
        abstract = True

class Engagement(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='engagements')
    date_of_function = models.DateField()
    day = models.CharField(max_length=10)
    lunch_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    lunch_min_pax_value = models.IntegerField(blank=True, null=True)
    hi_tea_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    hi_tea_min_pax_value = models.IntegerField(blank=True, null=True)
    dinner_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dinner_min_pax_value = models.IntegerField(blank=True, null=True)
    dj_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dj_value = models.IntegerField(blank=True, null=True)
    decor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    decor_value = models.IntegerField(blank=True, null=True)
    liquor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    liquor_value = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Sagan(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='sagans')
    date_of_function = models.DateField()
    day = models.CharField(max_length=10)
    lunch_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    lunch_min_pax_value = models.IntegerField(blank=True, null=True)
    hi_tea_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    hi_tea_min_pax_value = models.IntegerField(blank=True, null=True)
    dinner_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dinner_min_pax_value = models.IntegerField(blank=True, null=True)
    dj_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dj_value = models.IntegerField(blank=True, null=True)
    decor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    decor_value = models.IntegerField(blank=True, null=True)
    liquor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    liquor_value = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Roka(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='rokas')
    date_of_function = models.DateField()
    day = models.CharField(max_length=10)
    lunch_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    lunch_min_pax_value = models.IntegerField(blank=True, null=True)
    hi_tea_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    hi_tea_min_pax_value = models.IntegerField(blank=True, null=True)
    dinner_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dinner_min_pax_value = models.IntegerField(blank=True, null=True)
    dj_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dj_value = models.IntegerField(blank=True, null=True)
    decor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    decor_value = models.IntegerField(blank=True, null=True)
    liquor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    liquor_value = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Haldi(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='haldis')
    date_of_function = models.DateField()
    day = models.CharField(max_length=10)
    lunch_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    lunch_min_pax_value = models.IntegerField(blank=True, null=True)
    hi_tea_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    hi_tea_min_pax_value = models.IntegerField(blank=True, null=True)
    dinner_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dinner_min_pax_value = models.IntegerField(blank=True, null=True)
    dj_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dj_value = models.IntegerField(blank=True, null=True)
    decor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    decor_value = models.IntegerField(blank=True, null=True)
    liquor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    liquor_value = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Mehndi(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='mehndis')
    date_of_function = models.DateField()
    day = models.CharField(max_length=10)
    lunch_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    lunch_min_pax_value = models.IntegerField(blank=True, null=True)
    hi_tea_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    hi_tea_min_pax_value = models.IntegerField(blank=True, null=True)
    dinner_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dinner_min_pax_value = models.IntegerField(blank=True, null=True)
    dj_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dj_value = models.IntegerField(blank=True, null=True)
    decor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    decor_value = models.IntegerField(blank=True, null=True)
    liquor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    liquor_value = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Wedding(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='weddings')
    date_of_function = models.DateField()
    day = models.CharField(max_length=10)
    lunch_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    lunch_min_pax_value = models.IntegerField(blank=True, null=True)
    hi_tea_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    hi_tea_min_pax_value = models.IntegerField(blank=True, null=True)
    dinner_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dinner_min_pax_value = models.IntegerField(blank=True, null=True)
    dj_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dj_value = models.IntegerField(blank=True, null=True)
    decor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    decor_value = models.IntegerField(blank=True, null=True)
    liquor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    liquor_value = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    vedi_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    vedi_value = models.IntegerField(null=True, blank=True)

class Reception(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='receptions')
    date_of_function = models.DateField()
    day = models.CharField(max_length=10)
    lunch_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    lunch_min_pax_value = models.IntegerField(blank=True, null=True)
    hi_tea_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    hi_tea_min_pax_value = models.IntegerField(blank=True, null=True)
    dinner_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dinner_min_pax_value = models.IntegerField(blank=True, null=True)
    dj_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dj_value = models.IntegerField(blank=True, null=True)
    decor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    decor_value = models.IntegerField(blank=True, null=True)
    liquor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    liquor_value = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Corporate(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='corporates')
    date_of_function = models.DateField()
    day = models.CharField(max_length=10)
    lunch_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    lunch_min_pax_value = models.IntegerField(blank=True, null=True)
    hi_tea_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    hi_tea_min_pax_value = models.IntegerField(blank=True, null=True)
    dinner_min_pax_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dinner_min_pax_value = models.IntegerField(blank=True, null=True)
    dj_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    dj_value = models.IntegerField(blank=True, null=True)
    decor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    decor_value = models.IntegerField(blank=True, null=True)
    liquor_type = models.CharField(max_length=6, choices=[('yes', 'Yes'), ('no', 'No'), ('number', 'Number')], default='no')
    liquor_value = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Rooms(StandardOccasion):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='rooms')
    number_of_pax = models.IntegerField()
    number_of_rooms = models.IntegerField()
    plan = models.CharField(max_length=255)

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
