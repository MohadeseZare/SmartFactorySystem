from rest_framework import serializers
from device.models import Device, DeviceType, HistoryData, ErrorLine


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class ReportDeviceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class ErrorDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorLine
        fields = '__all__'

    def create(self, validated_data):
        error = super().create(validated_data)
        error.save()
        return error