# from django.contrib import admin
# from .models import *


# class GenderAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name')


# class OperationsTypeAdmin(admin.ModelAdmin):
    # list_display = ('id', 'type', 'name')


# class PermissionsAdmin(admin.ModelAdmin):
    # list_display = (
        # 'id',
        # 'name',
        # 'object',
        # 'created_at',
        # 'update_at',
        # 'deleted_at'
    # )


# class RolesAdmin(admin.ModelAdmin):
    # list_display = (
        # 'id',
        # 'name',
        # 'is_predefined',
        # 'description',
        # 'created_at',
        # 'update_at',
        # 'deleted_at'
    # )


# class PermissionsRoleAdmin(admin.ModelAdmin):
    # list_display = (
        # 'role_id',
        # 'permissions_id',
        # 'operation_type_id'
    # )


# class UsersAdmin(admin.ModelAdmin):
    # list_display = (
        # 'user_id',
        # 'gender_id',
        # 'phone_number',
        # 'city',
        # 'address',
        # 'deleted_at',
        # 'created_at',
        # 'updated_at',
        # 'get_roles'
    # )

    # def get_roles(self, obj):
        # return ",".join([str(p) for p in obj.role.all()])


# admin.site.register(Gender, GenderAdmin)
# admin.site.register(OperationsTypes, OperationsTypeAdmin)
# admin.site.register(Permissions, PermissionsAdmin)
# admin.site.register(Roles, RolesAdmin)
# admin.site.register(PermissionsRole, PermissionsRoleAdmin)
# admin.site.register(Users, UsersAdmin)
