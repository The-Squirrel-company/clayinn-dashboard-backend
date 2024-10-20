from django.urls import path
from .views import LeadListView, LeadCreateView, LeadDetailView

urlpatterns = [
    path('leads/<str:location_id>/', LeadListView.as_view(), name='lead-list'),
    path('leads/create/', LeadCreateView.as_view(), name='lead-create'),
    path('leads/detail/<int:lead_number>/', LeadDetailView.as_view(), name='lead-detail'),
]
