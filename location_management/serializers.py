from rest_framework import serializers
from .models import Location
from user_management.models import User

class LocationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name', 'email']

class LocationSerializer(serializers.ModelSerializer):
    location_admin = LocationAdminSerializer(read_only=True)

    class Meta:
        model = Location
        fields = ['loc_id', 'name', 'address', 'location_admin']

