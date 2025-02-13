from django.urls import path
from user_management import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterSuperAdmin  # Import other views as needed

urlpatterns = [
    path("test/", views.TestAPIView.as_view(), name="test"),
    path("login/", views.TokenView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path('locations/<str:loc_id>/sales-persons/', views.SalesPersonManagement.as_view(), name='sales_person_list'),
    path('locations/<str:loc_id>/sales-persons/<str:user_id>/', views.SalesPersonDetail.as_view(), name='sales_person_detail'),
    path('register-super-admin/', RegisterSuperAdmin.as_view(), name='register_super_admin'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit-profile'),
    path('profile/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]
