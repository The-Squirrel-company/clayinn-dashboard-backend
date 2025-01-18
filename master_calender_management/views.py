from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from location_management.models import Location
from venue_management.models import Venue
from bookings_management.models import Booking
from rest_framework.permissions import IsAuthenticated
from calendar import monthrange

class LocationCalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, location_id):
        try:
            # Get month and year from query params
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

            # Get location and its venues
            location = Location.objects.get(loc_id=location_id)
            
            # Check if user has permission for this location
            if request.user.role in ['location-admin', 'sales-person']:
                if request.user.loc_id != location:
                    return Response(
                        {'error': 'You do not have permission to view calendar for this location'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )

            venues = Venue.objects.filter(location=location)

            # Get all bookings for this month at this location
            bookings = Booking.objects.filter(
                location=location,
                event_date__year=year,
                event_date__month=month
            ).select_related('venue', 'lead', 'occasion')

            # Get the number of days in the month
            _, days_in_month = monthrange(year, month)

            # Initialize calendar data structure
            calendar_data = {}
            
            # Initialize all dates in the month
            for day in range(1, days_in_month + 1):
                date_str = f"{year}-{month:02d}-{day:02d}"
                calendar_data[date_str] = {
                    "date": date_str,
                    "venues": {}
                }
                # Initialize all venues for this date
                for venue in venues:
                    calendar_data[date_str]["venues"][venue.venue_id] = {
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
                date_str = booking.event_date.strftime("%Y-%m-%d")
                venue_id = booking.venue.venue_id
                
                calendar_data[date_str]["venues"][venue_id]["slots"][booking.slot] = {
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
                "year": year,
                "month": month,
                "days": list(calendar_data.values())
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
