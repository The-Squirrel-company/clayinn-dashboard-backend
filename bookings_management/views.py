from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer, BookingDetailSerializer, BookingCreateSerializer
from django.db.models import Q
from datetime import datetime
from leads_management.views import LeadPagination

class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get the requested venue, date and slot
        venue = serializer.validated_data['venue']
        event_date = serializer.validated_data['event_date']
        requested_slot = serializer.validated_data['slot']

        # Check only for the specific slot requested
        existing_booking = Booking.objects.filter(
            venue=venue,
            event_date=event_date,
            slot=requested_slot
        ).first()
        
        if existing_booking:
            return Response(
                {
                    "error": f"This venue is already booked for {requested_slot} on {event_date}",
                    "booked_by": existing_booking.lead.name
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking = serializer.save()

        # Change the lead status to 'closed-won'
        lead = booking.lead
        lead.lead_status = 'closed_won'
        lead.save()

        return Response(
            BookingDetailSerializer(booking).data,
            status=status.HTTP_201_CREATED
        )

class BookingListView(generics.ListAPIView):
    serializer_class = BookingDetailSerializer
    pagination_class = LeadPagination

    def get_queryset(self):
        location_id = self.kwargs.get('location_id')
        queryset = Booking.objects.filter(location_id=location_id)

        # Filter by venue if provided
        venue_id = self.request.query_params.get('venue')
        if venue_id:
            queryset = queryset.filter(venue_id=venue_id)

        # Filter by booking number if provided
        booking_number = self.request.query_params.get('booking_number')
        if booking_number:
            queryset = queryset.filter(booking_number=booking_number)

        # Filter by start date if provided
        start_date = self.request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(event_date__gte=start_date)

        # Filter by end date if provided
        end_date = self.request.query_params.get('end_date')
        if end_date:
            queryset = queryset.filter(event_date__lte=end_date)

        return queryset

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer
    lookup_field = 'booking_number'
    lookup_url_kwarg = 'booking_number'

class BookingSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        date = request.query_params.get('date')
        venue = request.query_params.get('venue')
        
        bookings = Booking.objects.all()

        if query:
            bookings = bookings.filter(
                Q(lead__name__icontains=query) |
                Q(venue__name__icontains=query) |
                Q(location__name__icontains=query)
            )

        if date:
            try:
                search_date = datetime.strptime(date, '%Y-%m-%d').date()
                bookings = bookings.filter(event_date=search_date)
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if venue:
            bookings = bookings.filter(venue_id=venue)

        serializer = BookingDetailSerializer(bookings, many=True)
        return Response(serializer.data)

class BookingAvailabilityView(APIView):
    def get(self, request):
        date = request.query_params.get('date')
        venue = request.query_params.get('venue_id')

        if not date or not venue:
            return Response(
                {"error": "Both date and venue_id parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            search_date = datetime.strptime(date, '%Y-%m-%d').date()
            
            # Get existing bookings for this date and venue
            existing_bookings = Booking.objects.filter(
                venue_id=venue,
                event_date=search_date
            ).select_related('lead')

            # Initialize availability dict
            availability = {
                'afternoon': {'available': True, 'booked_by': None},
                'evening': {'available': True, 'booked_by': None}
            }
            
            # Update booked slots
            for booking in existing_bookings:
                availability[booking.slot] = {
                    'available': False,
                    'booked_by': booking.lead.name,
                    'booking_number': booking.booking_number
                }

            return Response({
                "date": date,
                "venue_id": venue,
                "slots": {
                    "afternoon": {
                        "name": "Afternoon",
                        "status": availability['afternoon']
                    },
                    "evening": {
                        "name": "Evening",
                        "status": availability['evening']
                    }
                },
                "message": "A venue can be booked for both afternoon and evening slots"
            })

        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )
