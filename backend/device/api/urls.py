from django.urls import path
from .views import *

urlpatterns = [

    path('device/', DeviceView.as_view(), name='api-device'),
    path('device/<int:id>/', DetailDeviceView.as_view(), name='api-device-detail'),
    path('line-device/', LineDeviceView.as_view(), name='api-line-device'),
    path('report/', ReportDeviceView.as_view(), name='api-report'),
    # path('report/<int:id>/', .as_view(), name='api-report-log-details'),
    # path('report/excel/', .as_view(), name='api-report-excel'),
    # path('report/log/', .as_view(), name='api-report-log'),
    # path('receive-data/', .as_view(), name='api-receive-data'),
    path('live_data/', LiveDataView.as_view(), name='api-dashboard'),
    path('line_live_data/<product_line_id>', TileLiveView.as_view(), name='api-tile-dashboard'),

    path('tile_degree/', TileDegreeView.as_view(), name='api-tile-daily-static'),
    path('log_data/', LogDataView.as_view(), name='api-tile-log-data'),

    path('tile_degree_file/', TileDegreeGetExcelView.as_view(), name='api-tile-degree-excel'),
    path('log_data_file/', LogDataGetExcelView.as_view(), name='api-tile-log-data-excel'),

    path('add_error/', AddErrorView.as_view(), name='api-tile-add-error')
]
