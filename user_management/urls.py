from django.urls import path
from user_management import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("test/", views.TestAPIView.as_view(), name="test"),
    path("login/", views.TokenView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path('locations/<str:loc_id>/sales-persons/', views.SalesPersonManagement.as_view(), name='sales_person_list'),
    path('locations/<str:loc_id>/sales-persons/<str:user_id>/', views.SalesPersonDetail.as_view(), name='sales_person_detail'),
]
