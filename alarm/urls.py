from django.urls import path
from .views import *

urlpatterns = [
    path('create_alarm/', CreateAlarm.as_view(), name="create-alarm-api"),
    path('alarm_list/', ViewAlarm.as_view(), name='view-alarms')
]
