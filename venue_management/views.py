from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Venue
from location_management.models import Location
from .serializers import VenueSerializer
from bookings_management.models import Booking
from datetime import datetime
from django.db.models import Q
from calendar import monthrange

class VenueManagement(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, loc_id):
        try:
            location = Location.objects.get(loc_id=loc_id)
            
            # Check if user has permission for this location
            if request.user.role in ['location-admin', 'sales-person']:
                if request.user.loc_id != location:
                    return Response(
                        {'error': 'You do not have permission to view venues for this location'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )

            venues = Venue.objects.filter(location=location)
            serializer = VenueSerializer(venues, many=True)
            return Response(serializer.data)

        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, loc_id):
        try:
            location = Location.objects.get(loc_id=loc_id)
            
            # Check if user has permission for this location
            if request.user.role == 'location-admin':
                if request.user.loc_id != location:
                    return Response(
                        {'error': 'You do not have permission to create venues for this location'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
            elif request.user.role == 'sales-person':
                return Response(
                    {'error': 'Sales persons cannot create venues'}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = VenueSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(location=location)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

class VenueDetail(APIView):
    permission_classes = [IsAuthenticated]

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

        # Check if user has permission for this location
        if request.user.role == 'location-admin':
            if request.user.loc_id != venue.location:
                return Response(
                    {'error': 'You do not have permission to update venues for this location'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        elif request.user.role == 'sales-person':
            return Response(
                {'error': 'Sales persons cannot update venues'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = VenueSerializer(venue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, loc_id, venue_id):
        venue = self.get_object(loc_id, venue_id)
        if not venue:
            return Response({'error': 'Venue not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if user has permission for this location
        if request.user.role == 'location-admin':
            if request.user.loc_id != venue.location:
                return Response(
                    {'error': 'You do not have permission to delete venues for this location'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        elif request.user.role == 'sales-person':
            return Response(
                {'error': 'Sales persons cannot delete venues'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        venue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VenueDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, venue_id):
        try:
            venue = Venue.objects.get(venue_id=venue_id)
            
            # Check if user has permission for this location
            if request.user.role in ['location-admin', 'sales-person']:
                if request.user.loc_id != venue.location:
                    return Response(
                        {'error': 'You do not have permission to view venues for this location'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )

            year = request.query_params.get('year')
            month = request.query_params.get('month')

            if not year or not month:
                return Response(
                    {"error": "Both year and month parameters are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                year = int(year)
                month = int(month)
                if not (1 <= month <= 12):
                    raise ValueError("Month must be between 1 and 12")
            except ValueError as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get bookings for specified month
            bookings = Booking.objects.filter(
                venue=venue,
                event_date__year=year,
                event_date__month=month
            ).select_related('lead').order_by('event_date')

            # Create calendar data only for booked dates
            calendar_data = {}
            
            for booking in bookings:
                date_str = str(booking.event_date)
                
                if date_str not in calendar_data:
                    calendar_data[date_str] = {
                        "afternoon": None,
                        "evening": None
                    }
                
                calendar_data[date_str][booking.slot] = {
                    "status": f"Booked by {booking.lead.hostname}",
                    "bg_color": venue.bg_color
                }

            response_data = {
                "venue_details": {
                    "venue_id": venue.venue_id,
                    "name": venue.name,
                    "location": venue.location.name,
                    "bg_color": venue.bg_color
                },
                "bookings": calendar_data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Venue.DoesNotExist:
            return Response(
                {"error": "Venue not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
