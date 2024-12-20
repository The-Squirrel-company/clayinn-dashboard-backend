from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Location
from user_management.models import User
from .serializers import LocationSerializer
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# Create your views here.

class SuperAdminPermission(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'super-admin'

class LocationManagement(APIView):
    permission_classes = [SuperAdminPermission]

    def post(self, request):
        name = request.data.get('name')
        address = request.data.get('address')
        admin_name = request.data.get('location_admin_name')
        admin_email = request.data.get('location_admin_email')
        admin_password = request.data.get('location_admin_password')

        if not all([name, address, admin_name, admin_email, admin_password]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a user with the given email already exists
        if User.objects.filter(email=admin_email).exists():
            return Response({'error': 'A user with this email already exists, location cannot be created'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create the location first
            location = Location(name=name, address=address)
            location.save()  # This will generate loc_id using the overridden save method

            # Now create the location admin user
            admin_user = User.objects.create_user(
                email=admin_email,
                name=admin_name,
                password=admin_password,
                role='location-admin',
                loc_id=location  # Set the foreign key to the newly created location
            )

            return Response({
                'message': 'Location and location admin created successfully',
                'location_id': location.loc_id,
                'admin_id': admin_user.user_id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, loc_id=None):
        if loc_id:
            try:
                location = Location.objects.get(loc_id=loc_id)
                serializer = LocationSerializer(location)
                return Response(serializer.data)
            except Location.DoesNotExist:
                return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            locations = Location.objects.all()
            serializer = LocationSerializer(locations, many=True)
            return Response(serializer.data)

    def put(self, request, loc_id):
        try:
            location = Location.objects.get(loc_id=loc_id)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LocationSerializer(location, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, loc_id):
        try:
            location = Location.objects.get(loc_id=loc_id)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            location.delete()
            return Response({'message': 'Location and associated venues and users deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Error deleting location: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteLocationAdmin(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, loc_id):
        try:
            location = Location.objects.get(loc_id=loc_id)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is allowed to delete an admin
        if request.user.role == 'location-admin' and request.user.loc_id != location:
            return Response({'error': 'You do not have permission to delete an admin for this location'}, status=status.HTTP_403_FORBIDDEN)

        # Find the location admin user
        try:
            admin_user = User.objects.get(role='location-admin', loc_id=location)
        except User.DoesNotExist:
            return Response({'error': 'No location admin found for this location'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the location admin user
        admin_user.delete()
        return Response({'message': 'Location admin deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class AddLocationAdmin(APIView):
    permission_classes = [SuperAdminPermission]

    def post(self, request, loc_id):
        try:
            location = Location.objects.get(loc_id=loc_id)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is allowed to add an admin
        if request.user.role == 'location-admin' and request.user.loc_id != location:
            return Response({'error': 'You do not have permission to add an admin to this location'}, status=status.HTTP_403_FORBIDDEN)

        admin_name = request.data.get('admin_name')
        admin_email = request.data.get('admin_email')
        admin_password = request.data.get('admin_password')

        if not all([admin_name, admin_email, admin_password]):
            return Response({'error': 'admin_name, admin_email, and admin_password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(admin_email)
        except ValidationError:
            return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=admin_email).exists():
            return Response({'error': 'A user with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_admin = User.objects.create_user(
                email=admin_email,
                name=admin_name,
                password=admin_password,
                role='location-admin',
                loc_id=location  # Associate the new admin with the location
            )

            return Response({
                'message': 'Location admin added successfully',
                'admin_id': new_admin.user_id,
                'location_id': location.loc_id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
