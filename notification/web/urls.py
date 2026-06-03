from django.urls import path, include

from . import views

app_name = 'notification_web'

urlpatterns = [
    path('notifications/<int:notifikasi_id>/', views.notification_redirect, name='notification_redirect'),
    path("<int:notifikasi_id>/", views.detail, name="detail"),
    path("", views.index, name="index"),
]