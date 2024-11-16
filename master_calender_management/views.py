from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from location_management.models import Location
from venue_management.models import Venue
from bookings_management.models import Booking

# Create your views here.

class LocationCalendarView(APIView):
    def get(self, request, location_id):
        try:
            # Get date from query params
            date_str = request.query_params.get('date')
            if not date_str:
                return Response(
                    {"error": "Date parameter is required (YYYY-MM-DD)"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                search_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get location and its venues
            location = Location.objects.get(loc_id=location_id)
            venues = Venue.objects.filter(location=location)

            # Get all bookings for this date at this location
            bookings = Booking.objects.filter(
                location=location,
                event_date=search_date
            ).select_related('venue', 'lead', 'occasion')

            # Prepare venue booking data
            venue_bookings = {}
            
            # Initialize all venues with empty slots
            for venue in venues:
                venue_bookings[venue.venue_id] = {
                    "venue_id": venue.venue_id,
                    "venue_name": venue.name,
                    "bg_color": venue.bg_color,
                    "slots": {
                        "afternoon": None,
                        "evening": None
                    }
                }

            # Fill in the bookings
            for booking in bookings:
                venue_bookings[booking.venue.venue_id]["slots"][booking.slot] = {
                    "booking_number": booking.booking_number,
                    "lead_name": booking.lead.hostname,
                    "occasion": booking.occasion.occasion_type,
                    "mobile": booking.lead.mobile
                }

            response_data = {
                "location": {
                    "id": location.loc_id,
                    "name": location.name
                },
                "date": date_str,
                "venues": list(venue_bookings.values())
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Location.DoesNotExist:
            return Response(
                {"error": "Location not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
