from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Lead, Occasion
from .serializers import LeadSerializer
from location_management.models import Location

# Create your views here.

class LeadPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100

class LeadListView(generics.ListAPIView):
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LeadPagination

    def get_queryset(self):
        location_id = self.kwargs.get('location_id')
        user = self.request.user
        
        # Start with base queryset
        queryset = Lead.objects.all()
        
        # Apply location and role-based filtering
        if user.role == 'super-admin':
            if location_id:
                queryset = queryset.filter(location_id=location_id)
        elif user.role == 'location-admin':
            queryset = queryset.filter(location_id=user.loc_id)
        elif user.role == 'sales-person':
            queryset = queryset.filter(sales_person=user)
        else:
            queryset = Lead.objects.none()

        # Filter by lead status if provided
        lead_status = self.request.query_params.get('status')
        if lead_status:
            queryset = queryset.filter(lead_status=lead_status)

        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(lead_entry_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(lead_entry_date__lte=end_date)

        return queryset

class LeadCreateView(generics.CreateAPIView):
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the sales person to the current user if they're a sales person
        if self.request.user.role == 'sales-person':
            serializer.save(sales_person=self.request.user)
        else:
            serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'sales_person': request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LeadDetailView(generics.RetrieveUpdateDestroyAPIView):
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
            return Response(
                {"detail": "Sales person cannot update a closed-won lead."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Only super-admin and location-admin can delete leads
        if request.user.role not in ['super-admin', 'location-admin']:
            return Response(
                {"detail": "You do not have permission to delete leads."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
