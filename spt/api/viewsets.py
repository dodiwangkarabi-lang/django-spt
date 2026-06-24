from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# models
from spt.models import PermohonanSPT, SPT
from workflow.models import Disposisi

# serializers
from spt.api.serializers import PermohonanSPTSerializer, SPTSerializer, SetujuiPermohonanSPTSerializer

# service
from core.workflows.services import WorkFlowService

class SPTViewSet(ModelViewSet):
    queryset = SPT.objects.all()
    serializer_class = SPTSerializer
    
    # @action(detail=True, methods=["post"], url_path="setujui-spt")
    # def setujui_spt(self, request, pk=None):
    #     spt = self.get_object()
        
    #     service = WorkFlowService(spt)
    #     result = service.setujui()
    #     result = self.get_serializer(result).data
        
    #     return Response({
    #         "message": "SPT berhasil disetujui",
    #         "success": True,
    #         "data": result
    #     }, status.HTTP_200_OK)
        
    @action(detail=True, methods=["post"], url_path="tolak-spt")
    def tolak_spt(self, request, pk=None):
        spt = self.get_object()
        
        service = WorkFlowService(spt)
        result = service.tolak(request.data.get("catatan"))
        result = self.get_serializer(result).data
        
        return Response({
            "message": "SPT berhasil ditolak",
            "success": True,
            "data": result
        }, status.HTTP_200_OK)
        
    @action(detail=True, methods=["post"], url_path="revisi-spt")
    def revisi_spt(self, request, pk=None):
        spt = self.get_object()
        
        service = WorkFlowService(spt)
        result = service.revisi(request.data.get("catatan"))
        result = self.get_serializer(result).data
        
        return Response({
            "message": "SPT berhasil direvisi",
            "success": True,
            "data": result
        }, status.HTTP_200_OK)
        
    @action(detail=True, methods=["post"], url_path="setujui-spt")
    def setujui_spt(self, request, pk=None):
        spt = self.get_object()
        
        service = WorkFlowService(spt)
        result = service.setujui()
        result = self.get_serializer(result).data
        
        return Response({
            "message": "SPT berhasil disetujui",
            "success": True,
            "data": result
        }, status.HTTP_200_OK)

class PermohonanSPTViewSet(ModelViewSet):
    queryset = PermohonanSPT.objects.all()
    serializer_class = PermohonanSPTSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=["post"], url_path="ajukan-permohonan")
    def ajukan_permohonan(self, request, pk=None):
        permohonan = self.get_object()
        
        service = WorkFlowService(permohonan)
        result = service.ajukan(request.user)
        result = self.get_serializer(result).data
        
        return Response({
            "message": "Permohonan berhasil diajukan",
            "success": True,
            "data": result
        }, status.HTTP_200_OK)
        
    @action(detail=True, methods=["post"], url_path="tolak-permohonan")
    def tolak_permohonan(self, request, pk=None):
        permohonan = self.get_object()
        
        service = WorkFlowService(permohonan)
        result = service.tolak(request.data.get("catatan"))
        result = self.get_serializer(result).data
        
        return Response({
            "message": "Permohonan berhasil ditolak",
            "success": True,
            "data": result
        }, status.HTTP_200_OK)
        
    @action(detail=True, methods=["post"], url_path="revisi-permohonan")
    def revisi_permohonan(self, request, pk=None):
        permohonan = self.get_object()
        
        service = WorkFlowService(permohonan)
        result = service.revisi(request.data.get("catatan"))
        result = self.get_serializer(result).data
        
        return Response({
            "message": "Permohonan berhasil direvisi",
            "success": True,
            "data": result
        }, status.HTTP_200_OK)
        
    def get_serializer_class(self):
        if self.action == "setujui_permohonan":
            return SetujuiPermohonanSPTSerializer
        
        return super().get_serializer_class()
        
    @action(detail=True, methods=["post"], url_path="setujui-permohonan")
    def setujui_permohonan(self, request, pk=None):
        
        # form data
        # disposisi_id = request.data.get("disposisi_id")
        disposisi_serializer = self.get_serializer(data=request.data)
        # disposisi_serializer = SetujuiPermohonanSPTSerializer(data=request.data)
        disposisi_serializer.is_valid(raise_exception=True)
        disposisi_id = disposisi_serializer.validated_data["disposisi_id"]
        
        # object
        disposisi = get_object_or_404(Disposisi, id=disposisi_id)
        spt = disposisi.spt
        permohonan = spt.permohonan_spt
        # permohonan = self.get_object()
        
        # service
        permohonan_svc = WorkFlowService(permohonan)
        spt_svc = WorkFlowService(spt)
        disposisi_svc = WorkFlowService(disposisi)
        
        # update status permohonan, spt, disposisi
        permohonan_svc.setujui()
        spt_svc.setujui_permohonan()
        disposisi_svc.setujui()
        
        # serializer
        result = PermohonanSPTSerializer(permohonan).data 
        
        return Response({
            "message": "Permohonan berhasil disetujui",
            "success": True,
            "data": result
        }, status.HTTP_200_OK)