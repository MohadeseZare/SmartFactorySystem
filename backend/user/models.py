from django.db import models
from django.contrib.auth.models import User


class Gender(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class OperationsTypes(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=150)


class Permissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    object = models.CharField(max_length=100)  # that use for details
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Roles(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    is_predefined = models.BooleanField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class PermissionsRole(models.Model):
    role_id = models.ForeignKey(to=Roles, on_delete=models.CASCADE,)
    permissions_id = models.ForeignKey(to=Permissions, on_delete=models.CASCADE)
    operation_type_id = models.ForeignKey(to=OperationsTypes, on_delete=models.CASCADE)


class Users(models.Model):
    user = models.OneToOneField(User, models.CASCADE, default=1)
    gender = models.ForeignKey(Gender, models.RESTRICT, null=True)
    phone_number = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=255, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    role = models.ManyToManyField(Roles)

    def __str__(self):
        return self.user.username

