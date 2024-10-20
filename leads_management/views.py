from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Lead
from .serializers import LeadSerializer

# Create your views here.

class LeadPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

class LeadListView(generics.ListAPIView):
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LeadPagination

    def get_queryset(self):
        user = self.request.user
        if user.role == 'super-admin':
            return Lead.objects.all()
        elif user.role == 'location-admin':
            return Lead.objects.filter(venue__location=user.loc_id)
        elif user.role == 'sales-person':
            return Lead.objects.filter(sales_person=user)
        return Lead.objects.none()

class LeadCreateView(generics.CreateAPIView):
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sales_person=self.request.user)

class LeadUpdateView(generics.UpdateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'lead_number'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'super-admin':
            return Lead.objects.all()
        elif user.role == 'location-admin':
            return Lead.objects.filter(venue__location=user.loc_id)
        elif user.role == 'sales-person':
            return Lead.objects.filter(sales_person=user)
        return Lead.objects.none()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
