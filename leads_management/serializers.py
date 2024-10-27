from rest_framework import serializers
from .models import Lead, Engagement, Wedding, Corporate, Mehndi, Sagan, Roka, Reception, Rooms, Haldi
from user_management.serializers import UserSerializer
from venue_management.models import Venue
from location_management.models import Location

class EngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engagement
        fields = ['date_of_function', 'day', 'lunch_min_pax_type', 'lunch_min_pax_value', 
                  'hi_tea_min_pax_type', 'hi_tea_min_pax_value', 'dinner_min_pax_type', 
                  'dinner_min_pax_value', 'dj_type', 'dj_value', 'decor_type', 'decor_value', 
                  'liquor_type', 'liquor_value', 'total']

class WeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = ['date_of_function', 'day', 'lunch_min_pax_type', 'lunch_min_pax_value', 
                  'hi_tea_min_pax_type', 'hi_tea_min_pax_value', 'dinner_min_pax_type', 
                  'dinner_min_pax_value', 'dj_type', 'dj_value', 'decor_type', 'decor_value', 
                  'liquor_type', 'liquor_value', 'total', 'vedi_type', 'vedi_value']

class CorporateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporate
        fields = ['date_of_function', 'day', 'lunch_min_pax_type', 'lunch_min_pax_value', 
                  'hi_tea_min_pax_type', 'hi_tea_min_pax_value', 'dinner_min_pax_type', 
                  'dinner_min_pax_value', 'dj_type', 'dj_value', 'decor_type', 'decor_value', 
                  'liquor_type', 'liquor_value', 'total']

class SaganSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sagan
        fields = ['date_of_function', 'day', 'lunch_min_pax_type', 'lunch_min_pax_value', 
                  'hi_tea_min_pax_type', 'hi_tea_min_pax_value', 'dinner_min_pax_type', 
                  'dinner_min_pax_value', 'dj_type', 'dj_value', 'decor_type', 'decor_value', 
                  'liquor_type', 'liquor_value', 'total']

class RokaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roka
        fields = ['date_of_function', 'day', 'lunch_min_pax_type', 'lunch_min_pax_value', 
                  'hi_tea_min_pax_type', 'hi_tea_min_pax_value', 'dinner_min_pax_type', 
                  'dinner_min_pax_value', 'dj_type', 'dj_value', 'decor_type', 'decor_value', 
                  'liquor_type', 'liquor_value', 'total']

class HaldiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Haldi
        fields = ['date_of_function', 'day', 'lunch_min_pax_type', 'lunch_min_pax_value', 
                  'hi_tea_min_pax_type', 'hi_tea_min_pax_value', 'dinner_min_pax_type', 
                  'dinner_min_pax_value', 'dj_type', 'dj_value', 'decor_type', 'decor_value', 
                  'liquor_type', 'liquor_value', 'total']

class MehndiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mehndi
        fields = ['date_of_function', 'day', 'lunch_min_pax_type', 'lunch_min_pax_value', 
                  'hi_tea_min_pax_type', 'hi_tea_min_pax_value', 'dinner_min_pax_type', 
                  'dinner_min_pax_value', 'dj_type', 'dj_value', 'decor_type', 'decor_value', 
                  'liquor_type', 'liquor_value', 'total']

class ReceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reception
        fields = ['date_of_function', 'day', 'lunch_min_pax_type', 'lunch_min_pax_value', 
                  'hi_tea_min_pax_type', 'hi_tea_min_pax_value', 'dinner_min_pax_type', 
                  'dinner_min_pax_value', 'dj_type', 'dj_value', 'decor_type', 'decor_value', 
                  'liquor_type', 'liquor_value', 'total']

class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ['number_of_pax', 'number_of_rooms', 'plan']

class LeadSerializer(serializers.ModelSerializer):
    engagements = EngagementSerializer(many=True, required=False)
    weddings = WeddingSerializer(many=True, required=False)
    corporates = CorporateSerializer(many=True, required=False)
    sagans = SaganSerializer(many=True, required=False)
    rokos = RokaSerializer(many=True, required=False)
    haldis = HaldiSerializer(many=True, required=False)
    mehndis = MehndiSerializer(many=True, required=False)
    receptions = ReceptionSerializer(many=True, required=False)
    rooms = RoomsSerializer(many=True, required=False)

    sales_person = UserSerializer(read_only=True)
    venue_id = serializers.CharField()
    location_id = serializers.CharField()

    class Meta:
        model = Lead
        fields = '__all__'

    def create(self, validated_data):
        venue_id = validated_data.pop('venue_id')
        location_id = validated_data.pop('location_id')

        # Directly assign the IDs to the foreign key fields
        lead = Lead.objects.create(
            sales_person=self.context['sales_person'],
            hostname=validated_data['hostname'],
            mobile=validated_data['mobile'],
            venue_id_id=venue_id,  # Use venue_id_id to directly assign the ID
            location_id_id=location_id,  # Use location_id_id to directly assign the ID
            lead_status=validated_data.get('lead_status', 'untouched'),
            call_status=validated_data.get('call_status', 'not_yet_call'),
            followup=validated_data.get('followup'),
            remark=validated_data.get('remark'),
            email=validated_data.get('email')
        )

        print("Lead created with lead number:", lead.lead_number)

        # Handle occasions
        self.create_occasions(lead, validated_data)

        return lead

    def create_occasions(self, lead, validated_data):
        if 'engagements' in validated_data:
            engagements_data = validated_data.pop('engagements')
            for engagement_data in engagements_data:
                Engagement.objects.create(lead=lead, **engagement_data)

        if 'weddings' in validated_data:
            weddings_data = validated_data.pop('weddings')
            for wedding_data in weddings_data:
                Wedding.objects.create(lead=lead, **wedding_data)

        if 'corporates' in validated_data:
            corporates_data = validated_data.pop('corporates')
            for corporate_data in corporates_data:
                Corporate.objects.create(lead=lead, **corporate_data)

        if 'sagans' in validated_data:
            sagans_data = validated_data.pop('sagans')
            for sagan_data in sagans_data:
                Sagan.objects.create(lead=lead, **sagan_data)

        if 'rokos' in validated_data:
            rokos_data = validated_data.pop('rokos')
            for roka_data in rokos_data:
                Roka.objects.create(lead=lead, **roka_data)

        if 'haldis' in validated_data:
            haldis_data = validated_data.pop('haldis')
            for haldi_data in haldis_data:
                Haldi.objects.create(lead=lead, **haldi_data)

        if 'mehndis' in validated_data:
            mehndis_data = validated_data.pop('mehndis')
            for mehndi_data in mehndis_data:
                Mehndi.objects.create(lead=lead, **mehndi_data)

        if 'receptions' in validated_data:
            receptions_data = validated_data.pop('receptions')
            for reception_data in receptions_data:
                Reception.objects.create(lead=lead, **reception_data)

        if 'rooms' in validated_data:
            rooms_data = validated_data.pop('rooms')
            for room_data in rooms_data:
                Rooms.objects.create(lead=lead, **room_data)

    def validate(self, data):
        if not self.instance and 'sales_person' not in self.context:
            raise serializers.ValidationError("Sales person is required")
        return data

class LeadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['lead_number', 'hostname', 'mobile', 'lead_status', 'call_status', 'followup']
