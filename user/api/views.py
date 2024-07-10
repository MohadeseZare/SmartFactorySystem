# import json

# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.utils.decorators import method_decorator
# from rest_framework import generics
# from django.middleware.csrf import get_token
# from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
# from django.views.decorators.http import require_POST
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework import status
# from django.contrib.auth.models import User
# from user.api.serializers import UserSerializer, UserInstance
# from user.models import Users
# from rest_framework.permissions import AllowAny
# from django.contrib import auth
# from django.http import HttpResponse, HttpResponseRedirect

# def get_csrf(request):
    # response = JsonResponse({'detail': 'CSRF cookie set'})
    # response['X-CSRFToken'] = get_token(request)
    # return response


# @api_view(['POST'])
# def login_view(request):
    # data = json.loads(request.body)
    # username = data.get('username')
    # password = data.get('password')

    # if username is None or password is None:
        # return JsonResponse({'detail': 'Please provide username and password.'}, status=400)

    # user = authenticate(username=username, password=password)

    # if user is None:
        # return JsonResponse({'detail': 'Invalid credentials.'}, status=400)

    # login(request, user)
    # return JsonResponse({'detail': 'Successfully logged in.'})


# def logout_view(request):
    # if not request.user.is_authenticated:
        # return JsonResponse({'detail': 'You\'re not logged in.'}, status=400)

    # logout(request)
    # return JsonResponse({'detail': 'Successfully logged out.'})


# @ensure_csrf_cookie
# def session_view(request):
    # if not request.user.is_authenticated:
        # return JsonResponse({'isAuthenticated': False})

    # return JsonResponse({'isAuthenticated': True})


# def whoami_view(request):
    # if not request.user.is_authenticated:
        # return JsonResponse({'isAuthenticated': False})

    # return JsonResponse({'username': request.user.username})


# @api_view(['POST'])
# def test(request):
    # user = User.objects.last()
    # print(request.body)
    # ser = UserSerializer(instance=UserInstance(user), data=request.data, partial=True)
    # if ser.is_valid():
        # ser.save()
        # return Response(ser.data, status=status.HTTP_200_OK)
    # return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


# class Signup(generics.CreateAPIView):
    # serializer_class = UserSerializer

    # def post(self, request, *args, **kwargs):
        # # user = User.objects.last()
        # print(request.body)
        # ser = UserSerializer(data=request.data, partial=True)
        # if ser.is_valid():
            # ser.save()
            # return Response(ser.data, status=status.HTTP_200_OK)
        # return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
