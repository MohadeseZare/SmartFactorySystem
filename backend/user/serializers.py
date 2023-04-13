from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from . import models


# Serialize role model class.
# class RoleSerializer(serializers.ModelSerializer):
#     id = serializers.CharField(read_only=True)
#
#     class Meta:
#         model = models.Roles
#         fields = ('id', 'name', 'is_predefined', 'description')
#
#     def update(self, instance, validated_data):
#         non_null_data = {}
#         for key, value in validated_data.items():
#             if value:
#                 non_null_data[key] = value
#         role = super().update(instance, non_null_data)
#         role.updated_at = timezone.now()
#         role.save()
#         return role


# only serialize data for authentication (django User model).
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


# serialize other user information.
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Users
        fields = (
            'username', "first_name", "last_name", "phone_number", "email", 'created_at')
        read_only_fields = ('username', 'created_at')

    def update(self, instance, validated_data):
        non_null_data = {}
        for key, value in validated_data.items():
            if value:
                non_null_data[key] = value
        user = super().update(instance, non_null_data)
        user.updated_at = timezone.now()
        user.save()
        return user

    def email_verification(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.save()
        return instance
