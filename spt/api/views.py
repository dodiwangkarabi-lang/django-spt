from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import FileResponse

class HealthCheckView(APIView):
    def get(self, request, format=None):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
    
class CetakLaporanPelaksaanTugas(APIView):
    def get(self, request, spt_id, format=None):
        response_data = {
            "success": True,
            "message": "berhasil dicetak",
            "data": {"spt_id": spt_id}
        }
        return Response(response_data, status=status.HTTP_200_OK)