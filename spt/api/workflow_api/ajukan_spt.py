# api/workflow_api/ajukan_spt.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# models
from spt.models import SPT
from spt.models import SPTStatus

from spt.services.workflow.spt_transition_service import (
    transition_spt
)



class AjukanSPTAPIView(APIView):

    def post(self, request, spt_id):

        spt = SPT.objects.get(id=spt_id)

        transition_spt(
            spt=spt,
            new_status=SPTStatus.PERMOHONAN_DIAJUKAN
        )

        return Response({
            "success": True,
            "message": "SPT berhasil diajukan"
        }, status=status.HTTP_200_OK)