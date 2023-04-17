from rest_framework import serializers
from factory.models import Factory, FactoryMember, Shift, ProductLine, ProductLinePart, ProductLinePart2, Settings, \
    SettingsType
from user import serializers as user


class FactorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Factory
        fields = '__all__'


class FactoryMemberSerializers(serializers.ModelSerializer):
    member = user.UserSerializer()

    class Meta:
        model = FactoryMember
        fields = '__all__'
        # depth = 1


class ProductLineSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductLine
        fields = '__all__'
        # Add a field of the query parameter to the post method data


class ProductLinePartSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductLinePart
        fields = '__all__'


class ProductLinePart2Serializers(serializers.ModelSerializer):
    class Meta:
        model = ProductLinePart2
        fields = '__all__'


class ShiftSerializers(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'


class SettingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'


class SettingsTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = SettingsType
        fields = '__all__'
