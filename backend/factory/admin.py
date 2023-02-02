from django.contrib import admin
from .models import *


class FactoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'owner', 'create', 'update', 'delete')


class ShiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'factory', 'start_at', 'ends_at')


class ProductLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'factory')


class ProductLinePartAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'product_line')


class ProductLinePart2Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'product_line_part')


class FactoryMemberAdmin(admin.ModelAdmin):
    list_display = ('factory', 'member', 'status')


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'factory', 'inputs')


class SettingsTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'field', 'syntax')


admin.site.register(Factory, FactoryAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(ProductLinePart, ProductLinePartAdmin)
admin.site.register(ProductLinePart2, ProductLinePart2Admin)
admin.site.register(FactoryMember, FactoryMemberAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(SettingsType, SettingsTypeAdmin)
