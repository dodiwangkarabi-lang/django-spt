from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

# serializers
from workflow.disposisi.api.serializers import DisposisiSerializer
from spt.spt.api.serializers import SPTSerializer

# selectors
from accounts.selectors.selectors import (
    get_kasubag_user,
    get_pegawai_user,
    get_pimpinan_user
)

# models
from workflow.models import Disposisi, DisposisiTipe
from django.contrib.auth.models import User
from spt.models import SPT, SPTLampiran, SPTStatus
from notification.models import Notification

# services
from workflow.disposisi.services import DisposisiServices
from spt.spt.services import (
    SPTServices
)
from accounts.services.auth_service import UserService
from notification.services.services import (
    NotificationService
)

# constants
from notification.constants.constants import (
    NotificationEventType
)

class DisposisiViewSet(ModelViewSet):
    queryset = Disposisi.objects.all()
    serializer_class = DisposisiSerializer
    
class DisposisiUpdateRevisiView(APIView):
    def post(self, request, disposisi_id):
        disposisi = get_object_or_404(Disposisi, pk=disposisi_id)
        spt = disposisi.spt
        pimpinan_user = get_pimpinan_user()
        
        data = request.data.copy()
        
        # validasi data spt
        spt_data_cleaned = SPTSerializer(data=spt)
        spt_data_cleaned.is_valid(raise_exception=True)
        
        spt = SPTServices.update_spt(spt, **spt_data_cleaned.validated_data)
        
        # update status disposisi
        disposisi = DisposisiServices.update_status_dan_perima(
            disposisi=disposisi,
            status=DisposisiTipe.REQUEST,
            penerima_user=pimpinan_user
        )
        
        return Response({
            "message": "Disposisi berhasil diupdate",
            "success": True,
            "data": None
        }, status=status.HTTP_200_OK)

    
class DisposisiCreateView(APIView):
    def post(self, request):
        data = request.data.copy()
        permohonan_id = int(request.data.get("permohonan_id"))
        # print("permohonan_id", permohonan_id)
        
        kasubag = User.objects.filter(groups__name="kasubag").first()
        
        data['dari_user'] =  request.user.id
        data['ke_user'] = kasubag.id
        data["status"] = DisposisiTipe.INSTRUKSI
        
        # validasi
        data_cleaned = DisposisiSerializer(data=data)
        data_cleaned.is_valid(raise_exception=True)
        
        with transaction.atomic():
            disposisi = DisposisiServices.create_disposisi(
                permohonan_id=permohonan_id, **data_cleaned.validated_data
            ) # ini akan membuat spt baru dan update status permohonan
            
            # data notifikasi
            data_notifikasi = {
                # "penerima": get_kasubag_user(),
                "pengirim": get_pimpinan_user(),
                "pesan": f"Disposisi: {disposisi.catatan}",
                "content_type": ContentType.objects.get_for_model(Disposisi),
                "object_id": disposisi.id,
                "event_type": NotificationEventType.DISPOSISI_CREATED,
                "judul": "Disposisi"
            }
            
            # kirim notifikasi
            NotificationService.kirim_pesan(
                pengirim=get_pimpinan_user(),
                daftar_penerima=[get_kasubag_user(), get_pegawai_user()],
                data_notifikasi=data_notifikasi
            )
            
        
        return Response({
            "message": "Disposisi berhasil dibuat",
            "success": True,
            "data": None
        }, status=status.HTTP_201_CREATED)
        
        