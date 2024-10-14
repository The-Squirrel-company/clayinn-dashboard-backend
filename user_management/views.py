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

class RegisterUser(APIView):
    def post(self, request):
        email = request.data.get('email')
        name = request.data.get('name')
        password = request.data.get('password')
        role = request.data.get('role', 'sales-person')

        if not email or not name or not password:
            return Response({'error': 'Email, name, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if role not in dict(User.ROLE_CHOICES):
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            new_user = User.objects.create_user(
                email=email,
                name=name,
                password=password,
                role=role
            )
            return Response({
                'message': 'User created successfully',
                'user_id': new_user.user_id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Error in creating user: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TokenObtainSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        print(email, password)
        if email and password:
            user = User.objects.filter(email=email).first()
            print(user)
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
