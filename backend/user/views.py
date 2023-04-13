from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import json

from . import serializers
from . import permissions
from . import models
from factory import models as facmodels
from factory.api import serializers as facserializers


# @api_view(['POST'])
# @permission_classes((AllowAny,))
# def create_user(request):
#     ser = serializers.UserSerializer(data=request.data)
#     if ser.is_valid():
#         ser.save()
#         user = models.User.objects.get(username=request.data['username'])
#         factory_member = facmodels.FactoryMember.objects.get(
#             member=User.objects.get(username=request.data['username']).id)
#         factory_member_ser = facserializers.FactoryMemberSerializers(factory_member)
#         refresh_token = RefreshToken.for_user(user)
#         access_token = AccessToken.for_user(user)
#         final_json = {}
#         for key in ser.data:
#             final_json[key] = ser.data[key]
#         final_json['refresh'] = str(refresh_token)
#         final_json['access'] = str(access_token)
#         final_json['allowed_factories'] = factory_member_ser['factory'].value
#         if len(factory_member_ser['factory'].value) <= 1:
#             final_json['allowed_sections'] = factory_member_ser['product_line_id'].value
#         else:
#             final_json['allowed_sections'] = 0
#         json_ = json.dumps(final_json)
#         json_loaded = json.loads(json_)
#         return Response(json_loaded, status=status.HTTP_201_CREATED)
#     else:
#         return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_user(request):
    ser = serializers.UserSerializer(data={'username': request.data['username'], 'password': request.data['password']})
    if ser.is_valid():
        ser.save()
        user = User.objects.get(username=request.data['username'])
        final_json = {}
        for key in ser.data:
            final_json[key] = ser.data[key]
        factory_member = facmodels.FactoryMember.objects.get(
            member=user.id)
        try:
            admin = facmodels.FactoryMember.objects.get(member=User.objects.get(username=request.user.username))
            admin_ser = facserializers.FactoryMemberSerializers(admin)
            if request.data['factory'] in admin_ser['factory'].value:
                factory = facmodels.Factory.objects.get(id=request.data['factory'])
                factory_member.factory.set(factory)
        except:
            user.delete()
            return Response({'error': 'factory not found!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            factory_member.product_line.set(request.data['sections'])
        except:
            user.delete()
            return Response({'error': 'section not found!'}, status=status.HTTP_400_BAD_REQUEST)

        factory_member_ser = facserializers.FactoryMemberSerializers(factory_member)

        final_json['allowed_factories'] = factory_member_ser['factory'].value
        final_json['allowed_sections'] = factory_member_ser['product_line'].value

        users_user = models.Users.objects.get(username_id=User.objects.get(username=request.data['username']).id)
        data2 = serializers.ProfileSerializer(request.data['user_credential'])
        try:
            ser = serializers.ProfileSerializer().update(users_user, data2.data)
        except:
            user.delete()
            return Response({'error': 'this email has used before!'}, status=status.HTTP_400_BAD_REQUEST)
        user_ser = serializers.ProfileSerializer(ser)

        final_json['user_credential'] = user_ser.data

        json_ = json.dumps(final_json)
        json_loaded = json.loads(json_)
        return Response(json_loaded, status=status.HTTP_201_CREATED)

    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny, ])
def login(request):
    if authenticate(username=request.data['username'], password=request.data['password']):
        user = models.User.objects.get(username=request.data['username'])
        ser = serializers.UserSerializer(user)
        users_user = models.Users.objects.get(username=ser['id'].value)
        users_user_ser = serializers.ProfileSerializer(users_user)
        factory_member = facmodels.FactoryMember.objects.get(member=user)
        factory_member_ser = facserializers.FactoryMemberSerializers(factory_member)
        refresh_token = RefreshToken.for_user(user)
        access_token = AccessToken.for_user(user)
        final_json = {}
        for key in ser.data:
            final_json[key] = ser.data[key]
        final_json['first_name'] = users_user_ser['first_name'].value
        final_json['last_name'] = users_user_ser['last_name'].value
        final_json['refresh'] = str(refresh_token)
        final_json['access'] = str(access_token)
        final_json['allowed_factories'] = []
        final_json['allowed_sections'] = []
        try:
            for factory in factory_member_ser['factory'].value:
                final_json['allowed_factories'].append(factory)

            if len(factory_member_ser['factory'].value) <= 1:
                for section in factory_member_ser['product_line'].value:
                    final_json['allowed_sections'].append(section)

            else:
                final_json['allowed_sections'] = 0
        except:
            final_json['allowed_factories'] = []
            final_json['allowed_sections'] = []
        ALL = facmodels.ProductLine.objects.get(name='ALL').id
        if ALL in factory_member_ser['product_line'].value:
            final_json['is_admin'] = True
        else:
            final_json['is_admin'] = False
        json_ = json.dumps(final_json)
        json_loaded = json.loads(json_)
        return Response(json_loaded, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'authentication failed'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny, ])
def profile(request):
    try:
        user = models.Users.objects.get(username_id=request.user.id)
        ser = serializers.ProfileSerializer(user)
        final_json = {}
        for key in ser.data:
            final_json[key] = ser.data[key]
        factory_member = facmodels.FactoryMember.objects.get(member=request.user.id)
        factory_member_ser = facserializers.FactoryMemberSerializers(factory_member)
        final_json['allowed_factories'] = factory_member_ser['factory'].value
        final_json['allowed_sections'] = factory_member_ser['product_line'].value
    except:
        return Response({"error": "User Not Found!"}, status=status.HTTP_404_NOT_FOUND)
    return Response(final_json, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def users_list(request, pk):
    try:
        user = models.Users.objects.get(id=pk)
        ser = serializers.ProfileSerializer(user)
        final_json = {}
        for key in ser.data:
            final_json[key] = ser.data[key]
        factory_member = facmodels.FactoryMember.objects.get(member=pk)
        factory_member_ser = facserializers.FactoryMemberSerializers(factory_member)
        final_json['allowed_factories'] = factory_member_ser['factory'].value
        final_json['allowed_sections'] = factory_member_ser['product_line'].value
        json_ = json.dumps(final_json)
        json_loaded = json.loads(json_)
    except:
        return Response({"error": "User Not Found!"}, status=status.HTTP_404_NOT_FOUND)
    return Response(json_loaded, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def users_list_all(request):
    admin = request.user.id
    try:
        admin_user = facmodels.FactoryMember.objects.get(member=admin)
    except:
        return Response({'error': 'bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    admin_ser = facserializers.FactoryMemberSerializers(admin_user)
    resp = {}
    for factory in admin_ser['factory'].value:
        resp[f'{factory}'] = []
        if "sections" in request.data:
            for sections in request.data['sections']:
                user_list = facmodels.FactoryMember.objects.filter(factory__id__icontains=factory,
                                                                   product_line__id__icontains=sections,
                                                                   status="ENABlED")
                user_list_ser = facserializers.FactoryMemberSerializers(user_list, many=True)
                resp[f'{factory}'].append({sections: user_list_ser.data})

        else:
            user_list = facmodels.FactoryMember.objects.filter(factory__id__icontains=factory)
            user_list_ser = facserializers.FactoryMemberSerializers(user_list, many=True)
            resp[f'{factory}'] = user_list_ser.data
    return Response(resp, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([AllowAny, ])
def update_user(request):
    try:
        user = models.Users.objects.get(username_id=User.objects.get(username=request.data['username']).id)
    except:
        return Response({"error": "User Not Found!"}, status=status.HTTP_404_NOT_FOUND)

    try:
        data2 = serializers.ProfileSerializer(request.data)
        ser = serializers.ProfileSerializer().update(user, data2.data)
        user_ser = serializers.ProfileSerializer(ser)
    except:
        return Response({'error': 'Email Has Used Before'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(user_ser.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'DELETE'])
@permission_classes([AllowAny, ])
def update_user_admin(request):
    try:
        user = models.Users.objects.get(username_id=User.objects.get(username=request.data['username']).id)
    except:
        return Response({"error": "User Not Found!"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        final_json = {}
        try:
            admin = facmodels.FactoryMember.objects.get(member=User.objects.get(username=request.user.username))
            admin_ser = facserializers.FactoryMemberSerializers(admin)
            if request.data['factory'] in admin_ser['factory'].value:
                factory = facmodels.Factory.objects.get(id=request.data['factory'])
                user.factory.set(factory)
        except:
            return Response({'error': 'factory not found!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user.product_line.set(request.data['sections'])
        except:
            return Response({'error': 'section not found!'}, status=status.HTTP_400_BAD_REQUEST)

        factory_member_ser = facserializers.FactoryMemberSerializers(user)

        final_json['allowed_factories'] = factory_member_ser['factory'].value
        final_json['allowed_sections'] = factory_member_ser['product_line'].value

        users_user = models.Users.objects.get(username_id=User.objects.get(username=request.data['username']).id)
        data2 = serializers.ProfileSerializer(request.data['user_credential'])
        try:
            ser = serializers.ProfileSerializer().update(users_user, data2.data)
        except:
            return Response({'error': 'this email has used before!'}, status=status.HTTP_400_BAD_REQUEST)
        user_ser = serializers.ProfileSerializer(ser)

        final_json['user_credential'] = user_ser.data
        return Response(user_ser.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        user = User.objects.get(username=request.data['username'])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
