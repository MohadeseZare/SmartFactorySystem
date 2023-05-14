from rest_framework import permissions
from django.contrib.auth.models import User
from factory import models as facmodels


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(username=request.query_params['username'])
        except:
            return False

        if request.user.is_superuser:
            return True

        if not request.user == user:
            return False
        else:
            return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        factory_member = facmodels.FactoryMember.objects.get(member=request.user.id,
                                                             product_line__name__icontains="ALL")
        if factory_member:
            return True
        else:
            return False


class IsActive(permissions.BasePermission):
    def has_permission(self, request, view):
        factory_member = facmodels.FactoryMember.objects.get(member=request.user.id)
        if factory_member.status == 'ENABLED':
            return True
        else:
            return False
