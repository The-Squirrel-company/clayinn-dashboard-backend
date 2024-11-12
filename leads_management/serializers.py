from rest_framework import serializers
from .models import Lead, Occasion

class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        exclude = ['lead', 'booking']

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
        fields = '__all__'
        read_only_fields = ['lead_number', 'lead_entry_date']

    def create(self, validated_data):
        occasions_data = validated_data.pop('occasions', [])
        lead = Lead.objects.create(**validated_data)
        
        for occasion_data in occasions_data:
            Occasion.objects.create(lead=lead, **occasion_data)
            
        return lead

    def update(self, instance, validated_data):
        occasions_data = validated_data.pop('occasions', None)
        
        # Update lead instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update occasions if provided
        if occasions_data is not None:
            # Remove existing occasions
            instance.occasions.all().delete()
            # Create new occasions
            for occasion_data in occasions_data:
                Occasion.objects.create(lead=instance, **occasion_data)

        return instance
