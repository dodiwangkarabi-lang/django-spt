from .views import UserViewSet, ProfileViewSet
from rest_framework.routers import DefaultRouter

from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path("user-aktif/", views.UserAktifView.as_view(), name="accounts_api_user_aktif"),
    path("user/", views.UserView.as_view(), name="accounts_api_user"),
    path("user/<int:user_id>/", views.UserDetailView.as_view(), name="accounts_api_user_detail"),
    path("token/", TokenObtainPairView.as_view(), name="accounts_api_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="accounts_api_token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="accounts_api_token_verify"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("akuns/", views.AkunListView.as_view(), name="akuns"),
    path("akuns/me/", views.AkunMeView.as_view(), name="akuns_me"),
]

urlpatterns += router.urls