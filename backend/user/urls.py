from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('signup/', views.create_user),
    path('email_verification/', views.email_verification),
    path('login/', TokenObtainPairView.as_view()),
    path('login1/', views.login),
    path('refresh_access/', TokenRefreshView.as_view()),
    path('profile/', views.profile),
    path('update/', views.update_user),
    path('user_list/<pk>', views.users_list),
    path('is_admin/', views.is_admin),
    path('create_role/', views.role_creation),
    path('update_role/', views.update_role),
    path('roles/', views.view_role),
    path('admin_allocate_role/', views.role_allocation),
    path('admin_user_update/', views.update_user_admin)

]
