from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user_management.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import permissions
from location_management.models import Location
from .serializers import UserSerializer
from django.db import IntegrityError

class TestAPIView(APIView):
    def get(self, request):
        return Response({'message': 'Hello, world!'}, status=status.HTTP_200_OK)

class TokenObtainSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                refresh = self.get_token(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return data
            else:
                raise serializers.ValidationError('No active account found with the given credentials')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_id"] = user.user_id
        token["name"] = user.name
        token["email"] = user.email
        token['role'] = user.role
        token['loc_id'] = user.loc_id.loc_id if user.loc_id else None  # Add loc_id to the token
        return token

class TokenView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer

class AdminPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in ['super-admin', 'location-admin']

class SalesPersonManagement(APIView):
    permission_classes = [AdminPermission]

    def post(self, request, loc_id):
        try:
            location = Location.objects.get(loc_id=loc_id)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == 'location-admin' and request.user.loc_id != location:
            return Response({'error': 'You do not have permission to add sales persons to this location'}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(role='sales-person', loc_id=location)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, loc_id):
        try:
            location = Location.objects.get(loc_id=loc_id)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == 'location-admin' and request.user.loc_id != location:
            return Response({'error': 'You do not have permission to view sales persons for this location'}, status=status.HTTP_403_FORBIDDEN)

        sales_persons = User.objects.filter(role='sales-person', loc_id=location)
        serializer = UserSerializer(sales_persons, many=True)
        return Response(serializer.data)

class SalesPersonDetail(APIView):
    permission_classes = [AdminPermission]

    def get_object(self, user_id, loc_id):
        try:
            return User.objects.get(user_id=user_id, role='sales-person', loc_id__loc_id=loc_id)
        except User.DoesNotExist:
            return None

    def put(self, request, loc_id, user_id):
        sales_person = self.get_object(user_id, loc_id)
        if not sales_person:
            return Response({'error': 'Sales person not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == 'location-admin' and request.user.loc_id != sales_person.loc_id:
            return Response({'error': 'You do not have permission to edit this sales person'}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(sales_person, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, loc_id, user_id):
        sales_person = self.get_object(user_id, loc_id)
        if not sales_person:
            return Response({'error': 'Sales person not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == 'location-admin' and request.user.loc_id != sales_person.loc_id:
            return Response({'error': 'You do not have permission to delete this sales person'}, status=status.HTTP_403_FORBIDDEN)

        sales_person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterSuperAdmin(APIView):
    def post(self, request):
        # Hardcoded super admin details
        super_admin_data = {
            'email': 'admin@clayinn.in',
            'name': 'Super Admin',
            'password': 'admin',  # You should use a strong password in production
            'role': 'super-admin'
        }

        try:
            # Check if a super admin already exists
            if User.objects.filter(role='super-admin').exists():
                return Response({'error': 'A super admin already exists'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the super admin user
            user = User.objects.create_user(**super_admin_data)
            user.is_staff = True
            user.is_superuser = True
            user.save()

            return Response({'message': 'Super admin created successfully'}, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({'error': 'A user with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

