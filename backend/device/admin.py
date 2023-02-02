from django.contrib import admin
from .models import *


class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'mac_address', 'port', 'position', 'data', 'create', 'update', 'product_line_part', 'device_type'
    )


class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description', 'create', 'update'
    )


class HistoryDataAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'device_id', 'data', 'date'
    )


class LineDeviceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'mac_address', 'create', 'update'
    )
#  'product_line_part', 'device_type',

admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(HistoryData, HistoryDataAdmin)
admin.site.register(LineDevice, LineDeviceAdmin)
