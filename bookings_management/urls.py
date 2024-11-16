from django.urls import path
from .views import (
    BookingCreateView,
    BookingListView,
    BookingDetailView,
    BookingSearchView,
    BookingAvailabilityView
)

urlpatterns = [   
    path('bookings/create/', 
         BookingCreateView.as_view(), 
         name='booking-create'),
    
    path('bookings/detail/<int:booking_number>/', 
         BookingDetailView.as_view(), 
         name='booking-detail'),
    
    path('bookings/get/<str:location_id>/', 
         BookingListView.as_view(), 
         name='booking-list'),
    
    path('bookings/delete/<int:booking_number>/', 
         BookingDetailView.as_view(), 
         name='booking-delete'),
    
    path('bookings/search/', 
         BookingSearchView.as_view(), 
         name='booking-search'),
    
    path('bookings/check-availability/', 
         BookingAvailabilityView.as_view(), 
         name='booking-availability'),
]
