from rest_framework import serializers
from .models import Lead, Engagement, Sagan, Roka, Haldi, Mehndi, Wedding, Reception, Rooms, Corporate, Visit, PostCallStatus

class EngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engagement
        exclude = ['lead']

class SaganSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sagan
        exclude = ['lead']

class RokaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roka
        exclude = ['lead']

class HaldiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Haldi
        exclude = ['lead']

class MehndiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mehndi
        exclude = ['lead']

class WeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        exclude = ['lead']

class ReceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reception
        exclude = ['lead']

class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        exclude = ['lead']

class CorporateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporate
        exclude = ['lead']

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        exclude = ['lead']

class PostCallStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCallStatus
        exclude = ['lead']

class LeadSerializer(serializers.ModelSerializer):
    engagements = EngagementSerializer(many=True, required=False)
    sagans = SaganSerializer(many=True, required=False)
    rokas = RokaSerializer(many=True, required=False)
    haldis = HaldiSerializer(many=True, required=False)
    mehndis = MehndiSerializer(many=True, required=False)
    weddings = WeddingSerializer(many=True, required=False)
    receptions = ReceptionSerializer(many=True, required=False)
    rooms = RoomsSerializer(many=True, required=False)
    corporates = CorporateSerializer(many=True, required=False)
    visits = VisitSerializer(many=True, required=False)
    post_call_statuses = PostCallStatusSerializer(many=True, required=False)

    class Meta:
        model = Lead
        fields = '__all__'

    def create(self, validated_data):
        occasions = {
            'engagements': validated_data.pop('engagements', []),
            'sagans': validated_data.pop('sagans', []),
            'rokas': validated_data.pop('rokas', []),
            'haldis': validated_data.pop('haldis', []),
            'mehndis': validated_data.pop('mehndis', []),
            'weddings': validated_data.pop('weddings', []),
            'receptions': validated_data.pop('receptions', []),
            'rooms': validated_data.pop('rooms', []),
            'corporates': validated_data.pop('corporates', []),
        }
        visits_data = validated_data.pop('visits', [])
        post_call_statuses_data = validated_data.pop('post_call_statuses', [])

        lead = Lead.objects.create(**validated_data)

        for occasion_type, occasion_data_list in occasions.items():
            for occasion_data in occasion_data_list:
                getattr(lead, occasion_type).create(**occasion_data)

        for visit_data in visits_data:
            Visit.objects.create(lead=lead, **visit_data)

        for post_call_status_data in post_call_statuses_data:
            PostCallStatus.objects.create(lead=lead, **post_call_status_data)

        return lead

    def update(self, instance, validated_data):
        occasions = {
            'engagements': validated_data.pop('engagements', []),
            'sagans': validated_data.pop('sagans', []),
            'rokas': validated_data.pop('rokas', []),
            'haldis': validated_data.pop('haldis', []),
            'mehndis': validated_data.pop('mehndis', []),
            'weddings': validated_data.pop('weddings', []),
            'receptions': validated_data.pop('receptions', []),
            'rooms': validated_data.pop('rooms', []),
            'corporates': validated_data.pop('corporates', []),
        }
        visits_data = validated_data.pop('visits', [])
        post_call_statuses_data = validated_data.pop('post_call_statuses', [])

        instance = super().update(instance, validated_data)

        instance.engagements.all().delete()
        instance.sagans.all().delete()
        instance.rokas.all().delete()
        instance.haldis.all().delete()
        instance.mehndis.all().delete()
        instance.weddings.all().delete()
        instance.receptions.all().delete()
        instance.rooms.all().delete()
        instance.corporates.all().delete()
        instance.visits.all().delete()
        instance.post_call_statuses.all().delete()

        for occasion_type, occasion_data_list in occasions.items():
            for occasion_data in occasion_data_list:
                getattr(instance, occasion_type).create(**occasion_data)

        for visit_data in visits_data:
            Visit.objects.create(lead=instance, **visit_data)

        for post_call_status_data in post_call_statuses_data:
            PostCallStatus.objects.create(lead=instance, **post_call_status_data)

        return instance
