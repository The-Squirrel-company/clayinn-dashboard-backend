from django.urls import path
from .views import LocationManagement, DeleteLocationAdmin, AddLocationAdmin

urlpatterns = [
    path('locations/', LocationManagement.as_view(), name='location_list'),
    path('locations/<str:loc_id>/', LocationManagement.as_view(), name='location_detail'),
    path('locations/<str:loc_id>/delete-admin/', DeleteLocationAdmin.as_view(), name='delete_location_admin'),
    path('locations/<str:loc_id>/add-admin/', AddLocationAdmin.as_view(), name='add_location_admin'),
]
