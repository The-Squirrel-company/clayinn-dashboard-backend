from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Lead
from .serializers import LeadSerializer, LeadListSerializer
from location_management.models import Location

# Create your views here.

class LeadPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

class LeadListView(generics.ListAPIView):
    serializer_class = LeadListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LeadPagination

    def get_queryset(self):
        user = self.request.user
        location_id = self.kwargs.get('location_id')
        
        location = get_object_or_404(Location, loc_id=location_id)
        
        queryset = Lead.objects.filter(location_id=location)
        
        if user.role == 'super-admin':
            return queryset
        elif user.role == 'location-admin':
            if user.loc_id == location.loc_id:
                return queryset
            else:
                return Lead.objects.none()
        elif user.role == 'sales-person':
            return queryset.filter(sales_person=user)
        return Lead.objects.none()

class LeadCreateView(generics.CreateAPIView):
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sales_person=self.request.user)

    def create(self, request, *args, **kwargs):
        print("here")
        print(request.data)        
        print("here2")

        serializer = self.get_serializer(data=request.data, context={'sales_person': request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LeadDetailView(generics.RetrieveUpdateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'lead_number'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'super-admin':
            return Lead.objects.all()
        elif user.role == 'location-admin':
            return Lead.objects.filter(location_id=user.loc_id)
        elif user.role == 'sales-person':
            return Lead.objects.filter(sales_person=user)
        return Lead.objects.none()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Check if the lead status is already 'closed-won'
        if instance.lead_status == 'closed-won' and request.user.role == 'sales-person':
            return Response({"detail": "Sales person cannot update a closed-won lead."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
