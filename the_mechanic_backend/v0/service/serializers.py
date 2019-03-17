from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers

from the_mechanic_backend.apps.service.models import GeneralService, SubService, ServiceType, Service
from the_mechanic_backend.v0.utils import AppUtils


class GeneralServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralService
        fields = ('__all__',)


class SubServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubService
        fields = ('__all__',)


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ('__all__')


class ListServiceSerializer(serializers.ModelSerializer):
    booking_id = serializers.SerializerMethodField()
    vehicle_name = serializers.SerializerMethodField()
    vehicle_color = serializers.SerializerMethodField()
    vehicle_number = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()

    def get_booking_id(self, obj):
        return f'{obj.id:04}'

    def get_vehicle_name(self, obj):
        return AppUtils().get_vehicle_full_name(obj.vehicle)

    def get_vehicle_color(self, obj):
        return obj.vehicle.vehicle_color

    def get_vehicle_number(self, obj):
        return obj.vehicle.vehicle_number.upper()

    def get_services(self, obj):
        return ', '.join(x.service_name for x in obj.services.all())

    class Meta:
        model = Service
        fields = ('booking_id', 'vehicle_name', 'vehicle_color', 'vehicle_number', 'services')
