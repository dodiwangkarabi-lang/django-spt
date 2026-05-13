from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from spt.models import SPT

# from spt.serializers.spt_serializer import (
#     CreateSPTSerializer,
#     UpdateSPTSerializer,
#     SPTListSerializer,
#     SPTDetailSerializer,
# )

# serializers
from spt.serializers import SPTSerializer

# services
from spt.api.workflow_api.services import WorkFlowService

class WorkFlowSPTViewSet(ModelViewSet):
    queryset = SPT.objects.all()
    serializer_class = SPTSerializer
    
    @action(detail=True, methods=['post'], url_path="ajukan-spt")
    def ajukan_spt(self, request, pk=None):
        spt = self.get_object()
        
        service = WorkFlowService(spt)
        result = service.ajukan(request.user)
        result = self.get_serializer(result).data
        
        return Response({
            "message": "SPT berhasil diajukan",
            "success": True,
            "data": result
        }, status.HTTP_201_CREATED)
        
    @action(detail=True, methods=['post'], url_path="tolak-spt")
    def tolak_spt(self, request, pk=None):
        spt = self.get_object()
        
        service = WorkFlowService(spt)
        result = service.tolak(request.data.get("catatan"))
        result = self.get_serializer(result).data
        
        return Response({
            "message": "SPT berhasil ditolak",
            "success": True,
            "data": result
        }, status.HTTP_201_CREATED)
        
    @action(detail=True, methods=['post'], url_path="setujui-spt")
    def setujui_spt(self, request, pk=None):
        spt = self.get_object()
        
        service = WorkFlowService(spt)
        result = service.setujui()
        result = self.get_serializer(result).data
        
        return Response({
            "message": "SPT berhasil disetujui",
            "success": True,
            "data": result
        }, status.HTTP_201_CREATED)
        
    @action(detail=True, methods=['post'], url_path="revisi-spt")
    def revisi_spt(self, request, pk=None):
        spt = self.get_object()
        
        service = WorkFlowService(spt)
        result = service.revisi(request.data.get("catatan"))
        result = self.get_serializer(result).data
        
        return Response({
            "message": "SPT berhasil direvisi",
            "success": True,
            "data": result
        }, status.HTTP_201_CREATED)


class SPTListCreateApi(APIView):

    def get(self, request):
        queryset = (
            SPT.objects
            .all()
            .order_by("-created_at")
        )

        serializer = SPTSerializer(
            queryset,
            many=True
        )

        response_data = {
            "success": True,
            "data": serializer.data
        }

        return Response(response_data)

    def post(self, request):
        serializer = SPTSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        spt = serializer.save()

        response_data = {
            "success": True,
            "message": "SPT berhasil dibuat",
            "data": {
                "id": spt.id
            }
        }

        return Response(
            response_data,
            status=status.HTTP_201_CREATED
        )


class SPTDetailApi(APIView):

    def get_object(self, spt_id):
        return get_object_or_404(
            SPT,
            id=spt_id
        )

    def get(self, request, spt_id):
        spt = self.get_object(spt_id)

        serializer = SPTSerializer(spt)

        response_data = {
            "success": True,
            "data": serializer.data
        }

        return Response(response_data)

    def put(self, request, spt_id):
        spt = self.get_object(spt_id)

        serializer = SPTSerializer(
            spt,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response_data = {
            "success": True,
            "message": "SPT berhasil diupdate"
        }

        return Response(response_data)

    def delete(self, request, spt_id):
        spt = self.get_object(spt_id)

        spt.delete()

        response_data = {
            "success": True,
            "message": "SPT berhasil dihapus"
        }

        return Response(response_data)