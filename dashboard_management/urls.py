from django.urls import path
from .views import LocationDashboardView

urlpatterns = [
    path('locations/<str:location_id>/',
         LocationDashboardView.as_view(),
         name='location-dashboard'),
]
