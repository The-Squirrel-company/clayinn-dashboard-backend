from django.urls import path
from .views import (
    BookingListView,
    BookingCreateView,
    BookingDetailView,
    BookingUpdateView,
    BookingDeleteView
)

urlpatterns = [
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:booking_number>/', BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/<int:booking_number>/update/', BookingUpdateView.as_view(), name='booking-update'),
    path('bookings/<int:booking_number>/delete/', BookingDeleteView.as_view(), name='booking-delete'),
]
