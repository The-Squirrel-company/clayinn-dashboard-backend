from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Venue
from location_management.models import Location
from .serializers import VenueSerializer

class AdminPermission(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in ['super-admin', 'location-admin']

class VenueManagement(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, loc_id):
        try:
            location = Location.objects.get(loc_id=loc_id)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == 'location-admin' and request.user != location.location_admin:
            return Response({'error': 'You do not have permission to view venues for this location'}, status=status.HTTP_403_FORBIDDEN)

        venues = Venue.objects.filter(location=location)
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)

    def post(self, request, loc_id):
        try:
            location = Location.objects.get(loc_id=loc_id)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == 'location-admin' and request.user != location.location_admin:
            return Response({'error': 'You do not have permission to create venues for this location'}, status=status.HTTP_403_FORBIDDEN)

        serializer = VenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(location=location)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VenueDetail(APIView):
    permission_classes = [AdminPermission]

    def get_object(self, loc_id, venue_id):
        try:
            location = Location.objects.get(loc_id=loc_id)
            return Venue.objects.get(venue_id=venue_id, location=location)
        except (Location.DoesNotExist, Venue.DoesNotExist):
            return None

    def put(self, request, loc_id, venue_id):
        venue = self.get_object(loc_id, venue_id)
        if not venue:
            return Response({'error': 'Venue not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == 'location-admin' and request.user != venue.location.location_admin:
            return Response({'error': 'You do not have permission to update this venue'}, status=status.HTTP_403_FORBIDDEN)

        serializer = VenueSerializer(venue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, loc_id, venue_id):
        venue = self.get_object(loc_id, venue_id)
        if not venue:
            return Response({'error': 'Venue not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == 'location-admin' and request.user != venue.location.location_admin:
            return Response({'error': 'You do not have permission to delete this venue'}, status=status.HTTP_403_FORBIDDEN)

        venue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
