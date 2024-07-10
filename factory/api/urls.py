from django.urls import path
from .views import *

urlpatterns = [
    path('factory/', FactoryView.as_view(), name='api-factory'),
    path('factory/<int:id>/', DetailFactoryView.as_view(), name='api-factory-detail'),
    path('factory/member/', FactoryMemberView.as_view(), name='api-factory-member'),
    path('factory/member/<int:id>/', DeleteFactoryMemberView.as_view(), name='api-factory-member'),
    path('product-line/', ProductLineView.as_view(), name='api-product-line'),
    path('product-line/<int:id>/', DetailProductLineView.as_view(), name='api-product-line-detail'),
    path('product-line-part/', ProductLinePartView.as_view(), name='api-product-line-part'),
    path('product-line-part/<int:id>/', DetailProductLinePart.as_view(), name='api-product-line-part-detail'),
    path('product-line-part2/', ProductLinePart2View.as_view(), name='api-product-line-part-2'),
    path('product-line-part2/<int:id>/', DetailProductLinePart2.as_view(), name='api-product-line-part-2-detail'),
    path('shift/', ShiftView.as_view(), name='api-shift'),
    path('shift/<int:id>/', DetailShiftView.as_view(), name='api-shift'),
    path('setting/', SettingsView.as_view(), name='api-settings'),
    path('setting/<int:id>/', SettingsDetailView.as_view(), name='api-settings-detail'),
    path('type-setting/', SettingsTypeView.as_view(), name='api-type-of-settings'),
    path('type-setting/<int:id>/', DetailSettingsTypeView.as_view(), name='api-type-of-settings')
]

