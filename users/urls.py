from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('users/', user_list, name='user-list'),
    path('users/create/', user_create, name='user-create'),
    path('users/<uuid:pk>/', user_detail, name='user-detail'),
    path('users/<uuid:pk>/update/', user_update, name='user-update'),
    path('users/<uuid:pk>/delete/', user_delete, name='user-delete'),
    path('users/<uuid:pk>/approve/', update_user_approval, name='update-user-approval'),
    path('not-approved/', not_approved, name='not-approved'),
    path('change_password/', change_password, name='change-password'),
    # path('password-reset/', password_reset_request, name='password-reset-request'),
    path('users/password_reset/', password_reset_request, name='password_reset'),
    path('users/password_reset_confirm/<uidb64>/<token>/', password_reset_confirm, name='password-reset-confirm'),

]
