from rest_framework import serializers
from .models import *


class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarms
        fields = "__all__"
        depth = 1
