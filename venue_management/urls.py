from django.urls import path
from .views import VenueManagement, VenueDetail, VenueDetailView

urlpatterns = [
    path('locations/<str:loc_id>/venues/', VenueManagement.as_view(), name='venue_list'),
    path('locations/<str:loc_id>/venues/<str:venue_id>/', VenueDetail.as_view(), name='venue_detail'),
    path('venues/detail/<str:venue_id>/', VenueDetailView.as_view(), name='venue-detail'),
]

