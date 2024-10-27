from rest_framework import serializers
from .models import Lead, Engagement, Sagan, Roka, Haldi, Mehndi, Wedding, Reception, Rooms, Corporate, Visit, PostCallStatus
from user_management.serializers import UserSerializer
from venue_management.serializers import VenueSerializer
from location_management.serializers import LocationSerializer
from venue_management.models import Venue
from location_management.models import Location

class BaseOccasionSerializer(serializers.ModelSerializer):
    def validate(self, data):
        for field in ['lunch_min_pax', 'hi_tea_min_pax', 'dinner_min_pax', 'dj', 'decor', 'liquor']:
            type_field = f'{field}_type'
            value_field = f'{field}_value'
            if data.get(type_field) == 'number' and data.get(value_field) is None:
                raise serializers.ValidationError(f"{field} value is required when type is 'number'")
        return data

    class Meta:
        abstract = True
        fields = ['date_of_function', 'day', 'lunch_min_pax_type', 'lunch_min_pax_value', 'hi_tea_min_pax_type', 'hi_tea_min_pax_value', 'dinner_min_pax_type', 'dinner_min_pax_value', 'dj_type', 'dj_value', 'decor_type', 'decor_value', 'liquor_type', 'liquor_value', 'total']

class EngagementSerializer(BaseOccasionSerializer):
    class Meta(BaseOccasionSerializer.Meta):
        model = Engagement

class SaganSerializer(BaseOccasionSerializer):
    class Meta(BaseOccasionSerializer.Meta):
        model = Sagan

class RokaSerializer(BaseOccasionSerializer):
    class Meta(BaseOccasionSerializer.Meta):
        model = Roka

class HaldiSerializer(BaseOccasionSerializer):
    class Meta(BaseOccasionSerializer.Meta):
        model = Haldi

class MehndiSerializer(BaseOccasionSerializer):
    class Meta(BaseOccasionSerializer.Meta):
        model = Mehndi

class WeddingSerializer(BaseOccasionSerializer):
    class Meta(BaseOccasionSerializer.Meta):
        model = Wedding
        fields = BaseOccasionSerializer.Meta.fields + ['vedi_type', 'vedi_value']

class ReceptionSerializer(BaseOccasionSerializer):
    class Meta(BaseOccasionSerializer.Meta):
        model = Reception
        fields = BaseOccasionSerializer.Meta.fields + ['vedi_type', 'vedi_value']

class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ['date_of_function', 'day', 'number_of_pax', 'number_of_rooms', 'plan', 'total']

class CorporateSerializer(BaseOccasionSerializer):
    class Meta(BaseOccasionSerializer.Meta):
        model = Corporate
        fields = BaseOccasionSerializer.Meta.fields + ['vedi_type', 'vedi_value']

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        exclude = ['lead']

class PostCallStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCallStatus
        exclude = ['lead']

class LeadSerializer(serializers.ModelSerializer):
    engagements = EngagementSerializer(many=True, required=False)
    sagans = SaganSerializer(many=True, required=False)
    rokas = RokaSerializer(many=True, required=False)
    haldis = HaldiSerializer(many=True, required=False)
    mehndis = MehndiSerializer(many=True, required=False)
    weddings = WeddingSerializer(many=True, required=False)
    receptions = ReceptionSerializer(many=True, required=False)
    rooms = RoomsSerializer(many=True, required=False)
    corporates = CorporateSerializer(many=True, required=False)
    visits = VisitSerializer(many=True, required=False)
    post_call_statuses = PostCallStatusSerializer(many=True, required=False)
    sales_person = UserSerializer(read_only=True)
    venue_id = serializers.CharField()  # Accepts the string ID
    location_id = serializers.CharField()  # Accepts the string ID

    class Meta:
        model = Lead
        fields = '__all__'

    def create(self, validated_data):
        # Get the venue and location IDs from the validated data
        venue_id = validated_data.pop('venue_id')
        location_id = validated_data.pop('location_id')

        # Look up the Venue and Location instances
        venue_instance = Venue.objects.get(venue_id=venue_id)  # Assuming venue_id is the field name in Venue
        location_instance = Location.objects.get(loc_id=location_id)  # Assuming loc_id is the field name in Location

        # Create the Lead instance with the actual instances
        lead = Lead.objects.create(
            **validated_data,
            venue_id=venue_instance,
            location_id=location_instance
        )
        return lead

    def update(self, instance, validated_data):
        # Get the venue and location IDs from the validated data
        venue_id = validated_data.pop('venue_id', None)
        location_id = validated_data.pop('location_id', None)

        # Look up the Venue and Location instances if provided
        if venue_id:
            venue_instance = Venue.objects.get(venue_id=venue_id)
            instance.venue_id = venue_instance

        if location_id:
            location_instance = Location.objects.get(loc_id=location_id)
            instance.location_id = location_instance

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def validate(self, data):
        if not self.instance and 'sales_person' not in self.context:
            raise serializers.ValidationError("Sales person is required")
        return data

class LeadListSerializer(serializers.ModelSerializer):
    sales_person = UserSerializer(read_only=True)
    venue_id = serializers.CharField(source='venue_id.venue_id')  # Assuming venue_id is a string
    location_id = serializers.CharField(source='location_id.loc_id')  # Assuming loc_id is a string

    class Meta:
        model = Lead
        fields = ['lead_number', 'hostname', 'mobile', 'venue_id', 'location_id', 'lead_status', 'call_status', 'followup', 'remark', 'email', 'sales_person']
