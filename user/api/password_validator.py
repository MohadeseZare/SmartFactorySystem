# from django.contrib.auth.models import User
# from django.contrib.auth import password_validation
# from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
# from django.core import exceptions
# from django.db import transaction
# from user.models import Users


# class UserInstance:
    # def __init__(self, auth_user):
        # custom_user = auth_user.users

        # self.user = auth_user

        # self.id = auth_user.id
        # self.first_name = auth_user.first_name
        # self.last_name = auth_user.last_name
        # self.username = auth_user.username
        # self.email = auth_user.email
        # self.is_superuser = auth_user.is_superuser
        # self.address = custom_user.address
        # self.city = custom_user.city
        # self.phone_number = custom_user.phone_number
        # self.zip_code = custom_user.zip_code
        # self.country_id = custom_user.country_id
        # self.gender_id = custom_user.gender_id


# class UserSerializer(serializers.Serializer):
    # id = serializers.IntegerField(read_only=True)
    # first_name = serializers.CharField(required=True, min_length=2, max_length=150)
    # last_name = serializers.CharField(min_length=2, max_length=150, required=True)
    # username = serializers.CharField(min_length=5, max_length=150, required=True,
                                     # validators=[UniqueValidator(User.objects.all())]
                                     # )
    # email = serializers.EmailField(required=True, validators=[UniqueValidator(User.objects.all())])
    # is_superuser = serializers.BooleanField(default=False)
    # password = serializers.CharField(required=False, write_only=True, style={'input_type', 'password'}, min_length=8,
                                     # max_length=50)
    # password_confirmation = serializers.CharField(write_only=True, required=False)
    # address = serializers.CharField(required=False, allow_null=True, max_length=255)
    # city = serializers.CharField(required=False, allow_null=True, max_length=100)
    # phone_number = serializers.CharField(required=False, allow_null=True, max_length=30)
    # zip_code = serializers.CharField(required=False, allow_null=True, max_length=20)
    # country_id = serializers.IntegerField(required=False, allow_null=True)
    # gender_id = serializers.IntegerField(required=True)

    # def validate(self, data):
        # if self.instance is None:
            # keys = data.keys()
            # if 'password' not in keys:
                # raise serializers.ValidationError({
                    # 'password': 'This field is required.'
                # })
            # try:
                # password_validation.validate_password(data['password'])
                # if 'password_confirmation' not in keys:
                    # raise serializers.ValidationError({
                        # 'password_confirmation': 'This field is required.'
                    # })
                # if data['password'] != data['password_confirmation']:
                    # raise serializers.ValidationError({
                        # 'password_confirmation': 'Password and it\'s confirmation does not match.'
                    # })
            # except exceptions.ValidationError as e:
                # raise serializers.ValidationError({
                    # 'password': list(e.messages)
                # })
        # return data

    # @transaction.atomic
    # def create(self, validated_data):
        # user = User(
            # first_name=validated_data.get('first_name'),
            # last_name=validated_data.get('last_name'),
            # username=validated_data.get('username'),
            # email=validated_data.get('email'),
            # is_superuser=validated_data.get('is_superuser'),
        # )
        # user.set_password(validated_data.get('password'))
        # user.save()

        # user_profile = Users(
            # user=user,
            # address=validated_data.get('address'),
            # city=validated_data.get('city'),
            # phone_number=validated_data.get('phone_number'),
            # zip_code=validated_data.get('zip_code'),
            # country_id=validated_data.get('country_id'),
            # gender_id=validated_data.get('gender_id'),
        # )
        # user_profile.save()
        # return UserInstance(user)
        # pass

    # @transaction.atomic
    # def update(self, instance, validated_data):
        # user = instance.user
        # user.first_name = validated_data.get('first_name', instance.first_name)
        # user.last_name = validated_data.get('last_name', instance.last_name)
        # user.username = validated_data.get('username', instance.username)
        # user.email = validated_data.get('email', instance.email)
        # user.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        # user.save()

        # user_profile = user.users
        # user_profile.address = validated_data.get('address', instance.address)
        # user_profile.city = validated_data.get('city', instance.city)
        # user_profile.phone_number = validated_data.get('phone_number', instance.phone_number)
        # user_profile.zip_code = validated_data.get('zip_code', instance.zip_code)
        # user_profile.country_id = validated_data.get('country_id', instance.country_id)
        # user_profile.gender_id = validated_data.get('gender_id', instance.gender_id)
        # user.save()
        # return UserInstance(user)
        # pass
