from rest_framework import serializers
from .models import Lead, Engagement, Sagan, Roka, Haldi, Mehndi, Wedding, Reception, Rooms, Corporate, Visit, PostCallStatus
from user_management.serializers import UserSerializer
from venue_management.serializers import VenueSerializer
from location_management.serializers import LocationSerializer

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
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Lead
        fields = '__all__'

    def validate(self, data):
        if not self.instance and 'sales_person' not in self.context:
            raise serializers.ValidationError("Sales person is required")
        return data

    def create(self, validated_data):
        occasions = {
            'engagements': validated_data.pop('engagements', []),
            'sagans': validated_data.pop('sagans', []),
            'rokas': validated_data.pop('rokas', []),
            'haldis': validated_data.pop('haldis', []),
            'mehndis': validated_data.pop('mehndis', []),
            'weddings': validated_data.pop('weddings', []),
            'receptions': validated_data.pop('receptions', []),
            'rooms': validated_data.pop('rooms', []),
            'corporates': validated_data.pop('corporates', []),
        }
        visits_data = validated_data.pop('visits', [])
        post_call_statuses_data = validated_data.pop('post_call_statuses', [])

        lead = Lead.objects.create(**validated_data)

        for occasion_type, occasion_data_list in occasions.items():
            for occasion_data in occasion_data_list:
                getattr(lead, occasion_type).create(**occasion_data)

        for visit_data in visits_data:
            Visit.objects.create(lead=lead, **visit_data)

        for post_call_status_data in post_call_statuses_data:
            PostCallStatus.objects.create(lead=lead, **post_call_status_data)

        return lead

    def update(self, instance, validated_data):
        occasions = {
            'engagements': validated_data.pop('engagements', []),
            'sagans': validated_data.pop('sagans', []),
            'rokas': validated_data.pop('rokas', []),
            'haldis': validated_data.pop('haldis', []),
            'mehndis': validated_data.pop('mehndis', []),
            'weddings': validated_data.pop('weddings', []),
            'receptions': validated_data.pop('receptions', []),
            'rooms': validated_data.pop('rooms', []),
            'corporates': validated_data.pop('corporates', []),
        }
        visits_data = validated_data.pop('visits', [])
        post_call_statuses_data = validated_data.pop('post_call_statuses', [])

        instance = super().update(instance, validated_data)

        instance.engagements.all().delete()
        instance.sagans.all().delete()
        instance.rokas.all().delete()
        instance.haldis.all().delete()
        instance.mehndis.all().delete()
        instance.weddings.all().delete()
        instance.receptions.all().delete()
        instance.rooms.all().delete()
        instance.corporates.all().delete()
        instance.visits.all().delete()
        instance.post_call_statuses.all().delete()

        for occasion_type, occasion_data_list in occasions.items():
            for occasion_data in occasion_data_list:
                getattr(instance, occasion_type).create(**occasion_data)

        for visit_data in visits_data:
            Visit.objects.create(lead=instance, **visit_data)

        for post_call_status_data in post_call_statuses_data:
            PostCallStatus.objects.create(lead=instance, **post_call_status_data)

        return instance

class LeadListSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Lead
        fields = ['hostname', 'lead_number', 'lead_entry_date', 'mobile', 'followup', 'email', 'lead_status', 'venue', 'call_status', 'location']
