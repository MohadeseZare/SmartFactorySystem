from rest_framework.generics import *
from rest_framework.mixins import *
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *


class ViewAlarm(ListAPIView):
    serializer_class = AlarmSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.id
        return Alarms.objects.filter(user=user)



class CreateAlarm(ListCreateAPIView):
    queryset = Alarms.objects.all()
    serializer_class = AlarmSerializer
