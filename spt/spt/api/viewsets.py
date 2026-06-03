from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.db.models.functions import Lower
from django.contrib.contenttypes.models import ContentType

# models
from spt.models import SPT, SPTStatus
from workflow.models import Disposisi, DisposisiTipe

# serializers
from spt.spt.api.serializers import (
    SPTSerializer, SPTApprovalSerializer,
    SPTLampiranSerializer, SPTCatatanSerializer
)

# services
from spt.spt.services import (
    SPTServices, LampiranServices
)
from notification.services.services import NotificationService

# selectors
from spt.spt.selectors import (
    get_lampiran_by_spt
)
from accounts.selectors.selectors import (
    get_kasubag_user, get_pegawai_user, get_pimpinan_user
)

# constants
from notification.constants.constants import NotificationEventType

class KirimRevisiSPT(APIView):
    def post(self, request, spt_id=None):
        data = request.data.copy()
        spt = get_object_or_404(SPT, id=spt_id)
        spt = SPTServices.kirim_revisi_spt(
            data_spt=data, spt=spt
        )
        
        serializer = SPTSerializer(spt)
        
        return Response({
            "message": "SPT berhasil dikirim",
            "success": True,
            "data": serializer.data
        })

class ListLampiranView(APIView):
    def get(self, request, spt_id=None):
        daftar_lampiran = get_lampiran_by_spt(spt_id=spt_id)
        # order
        daftar_lampiran = daftar_lampiran.order_by(
            Lower('file')
        )
        
        serializer = SPTLampiranSerializer(daftar_lampiran, many=True)
        
        return Response({
            "message": "Lampiran berhasil diambil",
            "success": True,
            "data": serializer.data
        })

class HapusLampiranView(APIView):
    def post(self, request, lampiran_id=None):
        lampiran_service = LampiranServices.hapus_lampiran(
            lampiran_id=lampiran_id
        )
        
        return Response({
            "message": "Lampiran berhasil dihapus",
            "success": True,
            "data": None
        })

# lampiran
class SimpanBanyakLampiranView(APIView):
    def post(self, request, spt_id=None):
        spt = get_object_or_404(SPT, id=spt_id)
        daftar_lampiran = request.FILES.getlist("lampiran")
        
        lampiran_service = LampiranServices.simpan_banyak_lampiran(
            spt=spt,
            files=daftar_lampiran
        )
        
        return Response({
            "message": "Lampiran berhasil disimpan",
            "success": True,
            "data": None
        })


class SPTDetailAPIView(APIView):
    pass

class TolakSPTAPIView(APIView):
    def post(self, request, spt_id=None):
        # print(request.data)
        spt = SPT.objects.get(pk=spt_id)
        serializer = SPTApprovalSerializer(spt, data=request.data)
        if serializer.is_valid():
            # serializer.save()
            service = SPTServices.tolak_spt(spt=spt, catatan=request.data.get("catatan"))
            
            # notifikasi
            # data_notifikasi = {
            #     "pesan": f"SPT '{spt.judul}' telah ditolak ",
            #     "content_type": ContentType.objects.get_for_model(SPT),
            #     "object_id": spt.id,
            #     "event_type": NotificationEventType.SPT_REJECTED,
            #     "judul": "Penolakan SPT"
            # }
            # NotificationService.kirim_pesan(
            #     pengirim=get_pimpinan_user(),
            #     daftar_penerima = [get_kasubag_user(), get_pegawai_user()],
            #     data_notifikasi=data_notifikasi
            # )
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TerimaSPTAPIView(APIView):
    def post(self, request, spt_id=None):
        # print(request.data)
        spt = SPT.objects.get(pk=spt_id)
        serializer = SPTApprovalSerializer(spt, data=request.data)
        if serializer.is_valid():
            # serializer.save()
            service = SPTServices.terima_spt(spt=spt, catatan=request.data.get("catatan"))
            
            # notifikasi
            # data_notifikasi = {
            #     "pesan": f"SPT '{spt.judul}' telah diterima ",
            #     "content_type": ContentType.objects.get_for_model(SPT),
            #     "object_id": spt.id,
            #     "event_type": NotificationEventType.SPT_APPROVED,
            #     "judul": "Penerimaan SPT"
            # }
            # NotificationService.kirim_pesan(
            #     pengirim=get_pimpinan_user(),
            #     daftar_penerima = [get_kasubag_user(), get_pegawai_user()],
            #     data_notifikasi=data_notifikasi
            # )
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RevisiSPTAPIView(APIView):
    def post(self, request, spt_id=None):
        print(request.data)
        spt = SPT.objects.get(pk=spt_id)
        serializer = SPTCatatanSerializer(spt, data=request.data)
        if serializer.is_valid():
            
            # serializer.save()
            # diservice ini sudah ada kirim notifikasi
            spt = SPTServices.revisi_spt(spt=spt, catatan=request.data.get("catatan"))
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SPTListCreateWithDisposisiAPIView(APIView):
    def post(self, request, disposisi_id):
        disposisi = get_object_or_404(Disposisi, id=disposisi_id)
        serializer = SPTSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            spt = SPTServices.create_spt_with_disposisi(
                data=data, disposisi=disposisi, lampiran=data["lampiran"]
            )
            serializer = SPTSerializer(spt)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SPTUpdateAPIView(APIView):
    def post(self, request, pk=None):
        spt = SPT.objects.get(pk=pk)
        serializer = SPTSerializer(spt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)