from rest_framework import serializers
from .models import Venue

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['venue_id', 'name', 'location', 'bg_color']
        read_only_fields = ['venue_id', 'location']

