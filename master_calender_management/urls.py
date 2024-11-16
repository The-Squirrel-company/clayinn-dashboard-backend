from django.urls import path
from .views import LocationCalendarView

urlpatterns = [
    path('locations/<str:location_id>/', 
         LocationCalendarView.as_view(), 
         name='location-calendar'),
]
