from rest_framework import serializers
from .models import Booking
from leads_management.models import Lead
from venue_management.models import Venue
from location_management.models import Location
from user_management.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'booking_number', 'lead', 'venue', 'location', 
            'event_date', 'slot', 'occasion_type', 'occasion_id'
        ]
        read_only_fields = ['booking_number', 'booking_date', 'sales_person']

    def to_internal_value(self, data):
        # Convert the venue ID string to a Venue instance
        if 'venue' in data:
            try:
                venue = Venue.objects.get(venue_id=data['venue'])
                data['venue'] = venue.id
            except Venue.DoesNotExist:
                raise serializers.ValidationError({
                    'venue': 'Invalid venue ID'
                })

        # Convert the location ID string to a Location instance
        if 'location' in data:
            try:
                location = Location.objects.get(loc_id=data['location'])
                data['location'] = location.id
            except Location.DoesNotExist:
                raise serializers.ValidationError({
                    'location': 'Invalid location ID'
                })

        return super().to_internal_value(data)

    def validate(self, attrs):
        # Validate that the occasion exists for the given lead
        occasion_type = attrs.get('occasion_type')
        occasion_id = attrs.get('occasion_id')
        lead = attrs.get('lead')

        if not all([occasion_type, occasion_id, lead]):
            raise serializers.ValidationError('occasion_type, occasion_id and lead are required')

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
        try:
            model = apps.get_model(model_map[occasion_type])
            if not model.objects.filter(id=occasion_id, lead=lead).exists():
                raise serializers.ValidationError({
                    'occasion_id': f'Invalid occasion_id for the specified occasion_type and lead'
                })
        except KeyError:
            raise serializers.ValidationError({
                'occasion_type': 'Invalid occasion type'
            })

        # Check if venue is already booked for the date and slot
        venue = attrs.get('venue')
        event_date = attrs.get('event_date')
        slot = attrs.get('slot')

        if Booking.objects.filter(
            venue=venue,
            event_date=event_date,
            slot=slot
        ).exists():
            raise serializers.ValidationError({
                'venue': 'This venue is already booked for the specified date and slot'
            })

        return attrs
