from django.urls import path
from .views import VenueManagement, VenueDetail

urlpatterns = [
    path('locations/<str:loc_id>/venues/', VenueManagement.as_view(), name='venue_list'),
    path('locations/<str:loc_id>/venues/<str:venue_id>/', VenueDetail.as_view(), name='venue_detail'),
]

