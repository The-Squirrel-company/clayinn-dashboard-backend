from rest_framework import serializers
from .models import Lead, Occasion
from user_management.serializers import UserSerializer

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
    sales_person_details = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = [
            'lead_number', 'lead_entry_date', 'hostname', 'mobile',
            'lead_status', 'call_status', 'followup', 'email',
            'location_id', 'sales_person', 'sales_person_details', 'occasions', 'remark','lead_source'
        ]
        read_only_fields = ['lead_number', 'lead_entry_date']
        extra_kwargs = {
            'hostname': {'required': True},  # Required for creation
            'mobile': {'required': True},    # Required for creation
        }

    def get_sales_person_details(self, obj):
        if obj.sales_person:
            return {
                'name': obj.sales_person.name,
                'email': obj.sales_person.email,
                'mobile': obj.sales_person.mobile
            }
        return None

    def create(self, validated_data):
        occasions_data = validated_data.pop('occasions', [])
        lead = Lead.objects.create(**validated_data)
        
        for occasion_data in occasions_data:
            Occasion.objects.create(lead=lead, **occasion_data)
            
        return lead

    def update(self, instance, validated_data):
        # Update basic fields if provided
        for field in ['hostname', 'mobile', 'email', 'lead_status', 
                     'call_status', 'followup', 'location_id', 
                     'sales_person', 'remark', 'lead_source']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        
        # Handle occasions update if provided
        if 'occasions' in validated_data:
            new_occasions_data = validated_data.pop('occasions')
            existing_occasions = instance.occasions.all()
            
            # Match occasions based on occasion_type and date_of_function instead of ID
            for existing_occasion in existing_occasions:
                # Find matching occasion in new data
                matching_occasion = next(
                    (occ for occ in new_occasions_data 
                     if occ.get('occasion_type') == existing_occasion.occasion_type 
                     and str(occ.get('date_of_function')) == str(existing_occasion.date_of_function)),
                    None
                )
                
                if not matching_occasion:
                    # If no match found and occasion has bookings, raise error
                    if existing_occasion.bookings.exists():
                        raise serializers.ValidationError({
                            "error": f"Cannot delete occasion '{existing_occasion.occasion_type}' "
                                   f"for date {existing_occasion.date_of_function} "
                                   f"as it is linked to a booking."
                        })
                    else:
                        existing_occasion.delete()
                else:
                    # Update existing occasion
                    for key, value in matching_occasion.items():
                        setattr(existing_occasion, key, value)
                    existing_occasion.save()
                    # Remove from new_occasions_data to mark as processed
                    new_occasions_data.remove(matching_occasion)
            
            # Create any remaining new occasions
            for occasion_data in new_occasions_data:
                Occasion.objects.create(lead=instance, **occasion_data)
        
        instance.save()
        return instance
