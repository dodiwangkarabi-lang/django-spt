from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# content type
from django.contrib.contenttypes.models import ContentType

# models
from spt.models import PermohonanSPT, LampiranPermohonanSPT

# services
from spt.permohonan.services import PermohonanService
from notification.services.services import NotificationService

# serializers
from spt.permohonan.api.serializers import (
    PermohonanSPTSerializer,
    LampiranPermohonanSPTSerializer
)

# selectors
from accounts.selectors.selectors import (
    get_kasubag_user,
    get_pegawai_user,
    get_pimpinan_user
)

# constants
from notification.constants.constants import (
    NotificationEventType
)

from rest_framework.generics import ListAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class PermohonanSPTListView(ListAPIView):
    queryset = PermohonanSPT.objects.all()
    serializer_class = PermohonanSPTSerializer
    # filter_backends = [
    #     filters.SearchFilter,
    #     filters.OrderingFilter
    # ]
    # search_fields = ['judul', 'deskripsi']
    # ordering_fields = ['created_at']
    
    # dengan django filter
    filter_backends = [DjangoFilterBackend]
    filter_fields = [
        'status', 'judul', 'deskripsi'
    ]

class PermohonanApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        result = {
            "message": "Permohonan berhasil diajukan",
            "success": True,
        }
        return Response(result, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        # files = request.FILES
        
        data_permohonan = PermohonanSPTSerializer(data=data)
        # validasi
        data_permohonan.is_valid(raise_exception=True)
        data_permohonan = data_permohonan.validated_data
        data_permohonan["dibuat_oleh"] = request.user
        
        daftar_lampiran = data.getlist("lampiran[]")
        daftar_lampiran = [{"file": item, "keterangan": ""} for item in daftar_lampiran]
        
        permohonan = PermohonanService.create_permohonan_with_lampiran(data_permohonan, daftar_lampiran)
        
        # kirim notifikasi
        data_notifikasi = {
            "penerima": get_pimpinan_user(),
            "pengirim": get_kasubag_user(),
            "pesan": f"Pengajuan Permohonan Kegiatan '{permohonan.judul}'",
            "content_type": ContentType.objects.get_for_model(PermohonanSPT),
            "object_id": permohonan.id,
            "event_type": NotificationEventType.PERMOHONAN_CREATED,
            "judul": "Pengajuan Permohonan Kegiatan"
        }
        notifikasi = NotificationService.create(data_notifikasi)
        
        return Response({
            "message": "berhasil",
            "success": True,
            "data": None
        }, status=status.HTTP_201_CREATED)

class PermohonanSPTViewSet(ModelViewSet):
    queryset = PermohonanSPT.objects.all()
    serializer_class = PermohonanSPTSerializer
    
    # create permohonan with lampiran
    # @action(detail=True, methods=["post"], url_path="create-permohonan")
    # def create_permohonan(self, request, pk=None):

    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     data_permohonan = serializer.validated_data

    #     daftar_file = request.FILES.getlist("lampiran")
    #     daftar_keterangan = request.data.getlist("keterangan")

    #     daftar_lampiran = [
    #         {
    #             "file": item,
    #             "keterangan": daftar_keterangan[i]
    #         }
    #         for i, item in enumerate(daftar_file)
    #     ]

    #     permohonan = create_permohonan(
    #         data_permohonan=data_permohonan,
    #         daftar_lampiran=daftar_lampiran
    #     )

    #     output_serializer = self.get_serializer(permohonan)

    #     return Response(
    #         output_serializer.data,
    #         status=status.HTTP_201_CREATED
    #     )
        
    
class LampiranPermohonanSPTViewSet(ModelViewSet):
    queryset = LampiranPermohonanSPT.objects.all()
    serializer_class = LampiranPermohonanSPTSerializer