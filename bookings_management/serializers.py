from rest_framework import serializers
from .models import Booking
from leads_management.serializers import LeadSerializer, OccasionSerializer
from venue_management.serializers import VenueSerializer
from location_management.serializers import LocationSerializer
from user_management.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class BookingDetailSerializer(serializers.ModelSerializer):
    lead = LeadSerializer(read_only=True)
    occasion = OccasionSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    sales_person = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'lead',
            'occasion',
            'venue',
            'location',
            'sales_person',
            'event_date',
            'slot'
        ]
        # day will be auto-calculated

    def validate(self, data):
        # Check if venue is already booked for the given date and slot
        existing_booking = Booking.objects.filter(
            venue=data['venue'],
            event_date=data['event_date'],
            slot=data['slot']
        ).first()
        print(existing_booking)
        if existing_booking:
            raise serializers.ValidationError({
                "error": "This venue is already booked for the given date and slot"
            })

        return data
