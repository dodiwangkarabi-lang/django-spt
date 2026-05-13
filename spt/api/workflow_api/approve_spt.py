# api/workflow_api/approve_spt.py

from rest_framework.views import APIView
from rest_framework.response import Response

from spt.models import SPT

from spt.constants.spt_status import SPTStatus
from spt.services.workflow.spt_transition_service import (
    transition_spt
)


class ApproveSPTAPIView(APIView):

    def post(self, request, spt_id):

        spt = SPT.objects.get(id=spt_id)

        transition_spt(
            spt=spt,
            new_status=SPTStatus.DISETUJUI
        )

        return Response({
            "success": True,
            "message": "SPT berhasil disetujui"
        })