from django.urls import path, include
from notification.api import viewsets

app_name = 'notification_api'

urlpatterns = [
    path("pesan-dibaca/", viewsets.PesanDibacaAPIView.as_view(), name="pesan_dibaca"),
]