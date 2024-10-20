from django.urls import path
from .views import LeadListView, LeadCreateView, LeadUpdateView

urlpatterns = [
    path('leads/', LeadListView.as_view(), name='lead-list'),
    path('leads/create/', LeadCreateView.as_view(), name='lead-create'),
    path('leads/<int:lead_number>/update/', LeadUpdateView.as_view(), name='lead-update'),
]
