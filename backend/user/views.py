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
        user = models.User.objects.get(username=request.data['username'])
        refresh_token = RefreshToken.for_user(user)
        access_token = AccessToken.for_user(user)
        final_json = {}
        for key in ser.data:
            final_json[key] = ser.data[key]
        final_json['refresh'] = str(refresh_token)
        final_json['access'] = str(access_token)
        try:
            factory_member = facmodels.FactoryMember.objects.get(
                member=User.objects.get(username=request.data['username']).id)
            factory_member_ser = facserializers.FactoryMemberSerializers(factory_member)
            final_json['allowed_factories'] = factory_member_ser['factory'].value
            if len(factory_member_ser['factory'].value) <= 1:
                final_json['allowed_sections'] = factory_member_ser['product_line_id'].value
            else:
                final_json['allowed_sections'] = 0
        except:
            final_json['allowed_factories'] = []
            final_json['allowed_sections'] = []
        user = models.Users.objects.get(username_id=User.objects.get(username=request.data['username']).id)
        data2 = serializers.ProfileSerializer(request.data['user_credential'])
        ser = serializers.ProfileSerializer().update(user, data2.data)
        user_ser = serializers.ProfileSerializer(ser)
        # if not user_ser.is_valid():
        #     return Response({'error': 'Email Has Used Before'}, status=status.HTTP_400_BAD_REQUEST)

        final_json['user_credential'] = user_ser.data
        # return Response(user_ser.data, status=status.HTTP_200_OK)

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
        factory_member = facmodels.FactoryMember.objects.get(
            member=User.objects.get(username=request.data['username']).id)
        factory_member_ser = facserializers.FactoryMemberSerializers(factory_member)
        refresh_token = RefreshToken.for_user(user)
        access_token = AccessToken.for_user(user)
        final_json = {}
        for key in ser.data:
            final_json[key] = ser.data[key]
        final_json['refresh'] = str(refresh_token)
        final_json['access'] = str(access_token)
        final_json['allowed_factories'] = factory_member_ser['factory'].value
        if len(factory_member_ser['factory'].value) <= 1:
            final_json['allowed_sections'] = factory_member_ser['product_line_id'].value
        else:
            final_json['allowed_sections'] = 0
        user = models.Users.objects.get(username_id=User.objects.get(username=request.data['username']).id)
        user_ser = serializers.ProfileSerializer(user)
        admin_id = models.Roles.objects.get(name='admin').id
        for role in user_ser.data['role']:
            if role['id'] == str(admin_id):
                final_json['is_admin'] = True
            else:
                final_json['is_admin'] = False
        json_ = json.dumps(final_json)
        json_loaded = json.loads(json_)
        return Response(json_loaded, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'authentication failed'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny, ])
def profile(request):
    try:
        user = models.Users.objects.get(username_id=User.objects.get(username=request.data['username']).id)
        ser = serializers.ProfileSerializer(user)
    except:
        return Response({"error": "User Not Found!"}, status=status.HTTP_404_NOT_FOUND)
    return Response(ser.data, status=status.HTTP_200_OK)


# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny, ])
# def is_admin(request):
#     try:
#         user = models.Users.objects.get(username_id=User.objects.get(username=request.data['username']).id)
#         user_ser = serializers.ProfileSerializer(user)
#     except:
#         return Response({'error': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
#     admin_id = models.Roles.objects.get(name='admin').id
#     for role in user_ser.data['role']:
#         if role['id'] == str(admin_id):
#             return Response({'is_admin': 'true'})
#     return Response({'is_admin': 'False'})


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def users_list(request, pk):
    if pk != '0':
        try:
            user = models.Users.objects.get(pk=pk)
            ser = serializers.ProfileSerializer(user)
        except:
            return Response({"error": "User Not Found!"}, status=status.HTTP_404_NOT_FOUND)
    elif pk == '0':
        user = models.Users.objects.all()
        ser = serializers.ProfileSerializer(user, many=True)

    else:
        return Response({"error": "Bad request!"}, status=status.HTTP_404_NOT_FOUND)
    return Response(ser.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'DELETE'])
@permission_classes([AllowAny, ])
def update_user(request):
    try:
        user = models.Users.objects.get(username_id=User.objects.get(username=request.data['username']).id)
    except:
        return Response({"error": "User Not Found!"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        if 'role' in list(request.data.keys()):
            if request.data['role']:
                return Response({'error': "Role Can't Be Defined By User"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data2 = serializers.ProfileSerializer(request.data)
            ser = serializers.ProfileSerializer().update(user, data2.data)
            user_ser = serializers.ProfileSerializer(ser)
        except:
            return Response({'error': 'Email Has Used Before'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_ser.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        user = User.objects.get(username=request.data['username'])
        user.delete()
        return


@api_view(['PUT'])
@permission_classes([AllowAny, ])
def email_verification(request):
    try:
        user = models.Users.objects.get(username_id=User.objects.get(username=request.data['username']).id)
    except:
        return Response({"error": "User Not Found!"}, status=status.HTTP_404_NOT_FOUND)
    try:
        ser = serializers.ProfileSerializer().email_verification(user, request.data)
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
        # if 'role' in list(request.data.keys()):
        #     if request.data['role']:
        #         return Response({'error': "Role Can't Be Defined from this section."},
        #                         status=status.HTTP_400_BAD_REQUEST)
        data2 = serializers.ProfileSerializer(request.data)
        ser = serializers.ProfileSerializer().update(user, data2.data)
        user_ser = serializers.ProfileSerializer(ser)
        return Response(user_ser.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        user = User.objects.get(username=request.data['username'])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(["PUT"])
# @permission_classes([AllowAny, ])
# def role_allocation(request):
#     try:
#         user = models.Users.objects.get(username_id=User.objects.get(username=request.data['username']).id)
#     except:
#         return Response({"error": "User Not Found!"}, status=status.HTTP_404_NOT_FOUND)
#     try:
#         user.role.add(request.data['role'])
#         user_ser = serializers.ProfileSerializer(user)
#         return Response(user_ser.data, status=status.HTTP_200_OK)
#     except:
#         return Response({'error': 'Role Not Defined'}, status=status.HTTP_400_BAD_REQUEST)
#

@api_view(['POST'])
@permission_classes([AllowAny, ])
def role_creation(request):
    ser = serializers.RoleSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes([AllowAny, ])
def update_role(request):
    try:
        role = models.Roles.objects.get(id=request.data['id'])
    except:
        return Response({"error": "Role Not Found!"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        data2 = serializers.RoleSerializer(request.data)
        print(data2)
        ser = serializers.RoleSerializer().update(role, data2.data)
        role_ser = serializers.RoleSerializer(ser)
        return Response(role_ser.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        role = models.Roles.objects.get(id=request.data['id'])
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny, ])
def view_role(request):
    role = models.Roles.objects.all()
    role_ser = serializers.RoleSerializer(role, many=True)
    return Response(role_ser.data, status=status.HTTP_200_OK)
