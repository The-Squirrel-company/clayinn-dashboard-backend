from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from django.db.models import Count
from django.utils import timezone
from location_management.models import Location
from leads_management.models import Lead
from bookings_management.models import Booking

# Create your views here.

class LocationDashboardView(APIView):
    def get(self, request, location_id):
        try:
            location = Location.objects.get(loc_id=location_id)
            
            # Get current date and first day of current month
            today = timezone.now().date()
            first_day_of_month = today.replace(day=1)
            last_month_start = (first_day_of_month - timedelta(days=1)).replace(day=1)

            # Lead Statistics
            leads = Lead.objects.filter(location_id=location_id)
            leads_this_month = leads.filter(lead_entry_date__gte=first_day_of_month)
            leads_last_month = leads.filter(
                lead_entry_date__gte=last_month_start,
                lead_entry_date__lt=first_day_of_month
            )

            # Lead Status Statistics
            lead_status_stats = leads.values('lead_status').annotate(
                count=Count('lead_status')
            )
            
            # Call Status Statistics
            call_status_stats = leads.values('call_status').annotate(
                count=Count('call_status')
            )

            # Booking Statistics
            bookings = Booking.objects.filter(location_id=location_id)
            bookings_this_month = bookings.filter(booking_date__gte=first_day_of_month)
            bookings_last_month = bookings.filter(
                booking_date__gte=last_month_start,
                booking_date__lt=first_day_of_month
            )

            # Upcoming Bookings
            upcoming_bookings = bookings.filter(event_date__gte=today)

            # Occasion Type Statistics for this month
            occasion_stats = bookings_this_month.values(
                'occasion__occasion_type'
            ).annotate(count=Count('occasion__occasion_type'))

            # Format lead status stats with all possible statuses
            lead_status_counts = {
                'new': 0,
                'follow_up': 0,
                'converted': 0,
                'not_interested': 0,
                'cancelled': 0
            }
            for stat in lead_status_stats:
                if stat['lead_status'] in lead_status_counts:
                    lead_status_counts[stat['lead_status']] = stat['count']

            # Format call status stats with all possible statuses
            call_status_counts = {
                'pending': 0,
                'connected': 0,
                'not_reachable': 0,
                'wrong_number': 0
            }
            for stat in call_status_stats:
                if stat['call_status'] in call_status_counts:
                    call_status_counts[stat['call_status']] = stat['count']

            response_data = {
                "location": {
                    "id": location.loc_id,
                    "name": location.name
                },
                "leads": {
                    "total_leads": leads.count(),
                    "this_month": {
                        "total": leads_this_month.count(),
                        "percentage_change": calculate_percentage_change(
                            leads_this_month.count(),
                            leads_last_month.count()
                        )
                    },
                    "by_status": lead_status_counts,
                    "by_call_status": call_status_counts
                },
                "bookings": {
                    "total_bookings": bookings.count(),
                    "this_month": {
                        "total": bookings_this_month.count(),
                        "percentage_change": calculate_percentage_change(
                            bookings_this_month.count(),
                            bookings_last_month.count()
                        ),
                        "by_occasion": {
                            stat['occasion__occasion_type']: stat['count']
                            for stat in occasion_stats
                        }
                    },
                    "upcoming": {
                        "total": upcoming_bookings.count(),
                        "next_7_days": upcoming_bookings.filter(
                            event_date__lte=today + timedelta(days=7)
                        ).count()
                    }
                },
                "conversion_rate": {
                    "overall": calculate_percentage(
                        bookings.count(),
                        leads.count()
                    ),
                    "this_month": calculate_percentage(
                        bookings_this_month.count(),
                        leads_this_month.count()
                    )
                }
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

def calculate_percentage_change(new_value, old_value):
    if old_value == 0:
        return 100 if new_value > 0 else 0
    return round(((new_value - old_value) / old_value) * 100, 2)

def calculate_percentage(part, whole):
    if whole == 0:
        return 0
    return round((part / whole) * 100, 2)
