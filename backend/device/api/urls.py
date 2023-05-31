from django.urls import path
from .views import *

urlpatterns = [

    path('device/', DeviceView.as_view(), name='api-device'),
    path('device/<int:id>/', DetailDeviceView.as_view(), name='api-device-detail'),
    # path('line-device/', LineDeviceView.as_view(), name='api-line-device'),
    path('report/', ReportDeviceView.as_view(), name='api-report'),
    # path('report/<int:id>/', .as_view(), name='api-report-log-details'),
    # path('report/excel/', .as_view(), name='api-report-excel'),
    # path('report/log/', .as_view(), name='api-report-log'),
    # path('receive-data/', .as_view(), name='api-receive-data'),
    path('live_data/', LiveDataView.as_view(), name='api-dashboard'),
    path('fake_live_data/', FakeLiveView.as_view(), name='fake-live'),
    path('package_live_data/', PackageLiveView.as_view(), name='api-package-dashboard'),

    path('package_degree/', PackageDegreeView.as_view(), name='api-package-daily-static'),
    path('package_stoppage_time/', StoppageTimeView.as_view(), name='api-package-stoppage-time'),
    path('package_logdata/', LogDataView.as_view(), name='api-package-log-data'),
    path('package_error_frequency/', ErrorFrequencyView.as_view(), name='api-package-error-frequency'),

    path('package_degree_file/', PackageDegreeGetExcelView.as_view(), name='api-package-degree-excel'),
    path('package_stoppage_time_file/', StoppageTimeGetExcelView.as_view(), name='api-package-stoppage-time'),
    path('package_logdata_file/', LogDataGetExcelView.as_view(), name='api-package-log-data-excel'),
    path('package_error_frequency_file/', ErrorFrequencyGetExcelView.as_view(),
         name='api-package-error-frequency-excel'),

    path('add_error/', AddErrorView.as_view(), name='api-tile-add-error')
]
