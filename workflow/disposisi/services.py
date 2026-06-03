from django.db.models import Q, F
from django.db import transaction

# models
from workflow.models import Disposisi
from spt.models import SPTStatus

# services
from spt.permohonan.services import PermohonanService

class DisposisiServices:
    
    @staticmethod
    def create_disposisi_baru(spt, user):
        """
        Buat Disposisi Baru

        Args:
            spt (obj): instance object SPT
            user (obj): instance object User

        Returns:
            obj : instance object Disposisi
        
        Example:
            >>> disposisi = DisposisiServices.create_disposisi_baru(spt=spt, user=user)
            
        """
        disposisi = Disposisi.objects.create(spt=spt, ke_user=user)
        
        return disposisi
    
    @staticmethod
    def has_spt(disposisi_id) -> bool:
        disposisi = Disposisi.objects.get(id=disposisi_id)
        
        return bool(disposisi.spt)
    
    @staticmethod
    def create_disposisi(permohonan_id, **kwargs):
        disposisi = Disposisi.objects.create(**kwargs)
        
        # update status permohonan
        permohonan = PermohonanService.update_status(permohonan_id, SPTStatus.DISETUJUI)
        
        return disposisi
    

    @staticmethod
    @transaction.atomic
    def update_status_dan_perima(disposisi, status, penerima_user, catatan=None):
        disposisi.status = status
        disposisi.ke_user = penerima_user

        if catatan is not None:
            disposisi.catatan = catatan

        disposisi.save()
        return disposisi
    
    
    @staticmethod
    def update_status_disposisi(disposisi, status, catatan=None):
        disposisi.status = status

        if catatan is not None:
            disposisi.catatan = catatan

        disposisi.save()
        return disposisi
    
    @staticmethod
    def update_penerima(disposisi, penerima_user):
        disposisi.ke_user = penerima_user
        disposisi.save()
        
        return disposisi