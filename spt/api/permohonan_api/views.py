# from rest_framework.viewsets import ModelViewSet
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated

# # models
# from spt.models import PermohonanSPT

# # serializers
# from .serializers import PermohonanSPTSerializer

# # service
# from spt.api.workflow_api.services import WorkFlowService

# class PermohonanSPTViewSet(ModelViewSet):
#     queryset = PermohonanSPT.objects.all()
#     serializer_class = PermohonanSPTSerializer
#     permission_classes = [IsAuthenticated]
    
#     @action(detail=True, methods=["post"], url_path="ajukan-permohonan")
#     def ajukan_permohonan(self, request, pk=None):
#         permohonan = self.get_object()
        
#         service = WorkFlowService(permohonan)
#         result = service.ajukan(request.user)
#         result = self.get_serializer(result).data
        
#         return Response({
#             "message": "Permohonan berhasil diajukan",
#             "success": True,
#             "data": result
#         }, status.HTTP_201_CREATED)
        
#     @action(detail=True, methods=["post"], url_path="tolak-permohonan")
#     def tolak_permohonan(self, request, pk=None):
#         permohonan = self.get_object()
        
#         service = WorkFlowService(permohonan)
#         result = service.tolak(request.data.get("catatan"))
#         result = self.get_serializer(result).data
        
#         return Response({
#             "message": "Permohonan berhasil ditolak",
#             "success": True,
#             "data": result
#         }, status.HTTP_201_CREATED)
        
#     @action(detail=True, methods=["post"], url_path="revisi-permohonan")
#     def revisi_permohonan(self, request, pk=None):
#         permohonan = self.get_object()
        
#         service = WorkFlowService(permohonan)
#         result = service.revisi(request.data.get("catatan"))
#         result = self.get_serializer(result).data
        
#         return Response({
#             "message": "Permohonan berhasil direvisi",
#             "success": True,
#             "data": result
#         }, status.HTTP_201_CREATED)
        
#     @action(detail=True, methods=["post"], url_path="setujui-permohonan")
#     def setujui_permohonan(self, request, pk=None):
#         permohonan = self.get_object()
        
#         service = WorkFlowService(permohonan)
#         result = service.setujui()
#         result = self.get_serializer(result).data
        
#         return Response({
#             "message": "Permohonan berhasil disetujui",
#             "success": True,
#             "data": result
#         }, status.HTTP_201_CREATED)