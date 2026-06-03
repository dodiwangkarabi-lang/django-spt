# apiview
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# models
from notification.models import Notification

# selectors
from notification.selectors.selectors import (
    get_notification_by_id
)

# serializers
from notification.api.serializers import (
    NotificationSerializer
)

class PesanDibacaAPIView(APIView):
    def post(self, request, notifikasi_id):
        notification = get_notification_by_id(notifikasi_id)
        notification.dibaca = True
        notification.save()
        return Response({
            "success": True,
            "data": NotificationSerializer(notification).data,
            "pesan": "Pesan dibaca"
        })

