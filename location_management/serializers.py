from rest_framework import serializers
from .models import Location
from user_management.models import User
from user_management.serializers import UserSerializer  # Import the UserSerializer

class LocationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name', 'email']

class LocationSerializer(serializers.ModelSerializer):
    location_admin = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ['loc_id', 'name', 'address', 'location_admin']

    def get_location_admin(self, obj):
        # Fetch the location admin user associated with this location
        try:
            return UserSerializer(obj.users.filter(role='location-admin').first()).data
        except User.DoesNotExist:
            return None
