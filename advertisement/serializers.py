from rest_framework import serializers
from .models import Device,Media

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['device_id', 'orientation', 'resolution']

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['device']