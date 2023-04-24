from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('admin_create_user/', views.create_user),
    # path('create_user1/', views.create_user1),
    # path('email_verification/', views.email_verification),
    # path('login/', TokenObtainPairView.as_view()),
    path('login/', views.login),
    path('refresh/', TokenRefreshView.as_view()),
    path('profile/', views.profile),
    path('update/', views.update_user),
    path('admin_user_list_all/', views.users_list_all),
    path('admin_user_list/<pk>', views.users_list),
    # path('is_admin/', views.is_admin),
    # path('admin_create_role/', views.role_creation),
    # path('admin_update_role/', views.update_role),
    # path('admin_roles/', views.view_role),
    # path('admin_allocate_role/', views.role_allocation),
    path('admin_user_update/', views.update_user_admin),
    path('fu/first_user/', views.first_user)
]
