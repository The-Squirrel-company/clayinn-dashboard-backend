from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Booking
from .serializers import BookingSerializer

# Create your views here.

class BookingListView(generics.ListAPIView):
    """
    Get all bookings in a location
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'super-admin':
            return Booking.objects.all()
        elif user.role == 'location-admin':
            return Booking.objects.filter(location=user.loc_id)
        elif user.role == 'sales-person':
            return Booking.objects.filter(sales_person=user)
        return Booking.objects.none()

class BookingCreateView(generics.CreateAPIView):
    """
    Create new booking
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            sales_person=self.request.user,
            location=self.request.user.loc_id
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingDetailView(generics.RetrieveAPIView):
    """
    Get booking details using booking_number
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'booking_number'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'super-admin':
            return Booking.objects.all()
        elif user.role == 'location-admin':
            return Booking.objects.filter(location=user.loc_id)
        elif user.role == 'sales-person':
            return Booking.objects.filter(sales_person=user)
        return Booking.objects.none()

class BookingUpdateView(generics.UpdateAPIView):
    """
    Edit booking (sales person can't edit)
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'booking_number'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'super-admin':
            return Booking.objects.all()
        elif user.role == 'location-admin':
            return Booking.objects.filter(location=user.loc_id)
        return Booking.objects.none()

    def update(self, request, *args, **kwargs):
        if request.user.role == 'sales-person':
            return Response(
                {"detail": "Sales persons are not allowed to edit bookings."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

class BookingDeleteView(generics.DestroyAPIView):
    """
    Delete booking (sales person can't delete)
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'booking_number'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'super-admin':
            return Booking.objects.all()
        elif user.role == 'location-admin':
            return Booking.objects.filter(location=user.loc_id)
        return Booking.objects.none()

    def destroy(self, request, *args, **kwargs):
        if request.user.role == 'sales-person':
            return Response(
                {"detail": "Sales persons are not allowed to delete bookings."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
