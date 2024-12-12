from rest_framework import serializers
from .models import Lead, Occasion

class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        exclude = ['lead']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Only include relevant fields based on occasion type
        if instance.occasion_type == 'room':
            # Remove non-room fields
            fields_to_remove = ['lunch_pax', 'hi_tea_pax', 'dinner_pax', 
                              'dj_value', 'decor_value', 'liquor_value', 
                              'vedi_value', 'date_of_function', 'day']
            for field in fields_to_remove:
                representation.pop(field, None)
        else:
            # Remove room fields
            fields_to_remove = ['number_of_pax', 'number_of_rooms', 'plan']
            for field in fields_to_remove:
                representation.pop(field, None)
        return representation

class LeadSerializer(serializers.ModelSerializer):
    occasions = OccasionSerializer(many=True, required=False)

    class Meta:
        model = Lead
        fields = [
            'lead_number', 'lead_entry_date', 'hostname', 'mobile',
            'lead_status', 'call_status', 'followup', 'email',
            'location_id', 'sales_person', 'occasions'
        ]
        read_only_fields = ['lead_number', 'lead_entry_date']
        extra_kwargs = {
            'hostname': {'required': True},  # Required for creation
            'mobile': {'required': True},    # Required for creation
        }

    def create(self, validated_data):
        occasions_data = validated_data.pop('occasions', [])
        lead = Lead.objects.create(**validated_data)
        
        for occasion_data in occasions_data:
            Occasion.objects.create(lead=lead, **occasion_data)
            
        return lead

    def update(self, instance, validated_data):
        # Remove hostname and mobile from validated_data if not provided
        validated_data.pop('hostname', None)
        validated_data.pop('mobile', None)
        
        occasions_data = validated_data.pop('occasions', None)
        
        # Update lead instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update occasions if provided
        if occasions_data is not None:
            # Only delete occasions that are not linked to any bookings
            for occasion in instance.occasions.all():
                if not occasion.bookings.exists():
                    occasion.delete()
            
            # Create or update occasions
            for occasion_data in occasions_data:
                Occasion.objects.create(lead=instance, **occasion_data)

        return instance
