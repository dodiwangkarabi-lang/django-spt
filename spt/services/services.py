# data = request.POST.copy()
# lampiran = request.FILES.getlist("lampiran")

from django.db import transaction
from django.shortcuts import get_object_or_404

# services
from workflow.services import WorkFlowService

# models
from spt.models import (
    SPT, PermohonanSPT, SPTLampiran,
    JenisSurat, NomorSuratSequence
)

@transaction.atomic
def buat_surat_pernyataan_melaksananan_tugas(data, user):
    permohonan_spt_service = WorkFlowService(PermohonanSPT)
    permohonan_spt_service.buat_surat_pernyataan_melaksanakan_tugas(data, user)
    return True

def upload_lampiran_spt(spt_id, data): # spt -> Lampiran (1:N)
    """keterangan

    Args:
        spt_id (str): id dari spt
        data (any): data utama

    Returns:
        lampiran: instance object dari Lampiran
    """
    spt = get_object_or_404(SPT, id=spt_id)
    lampiran = SPTLampiran.objects.create(
        spt=spt,
        file=data.get("file"),
        keterangan=data.get("keterangan")
    )
    return lampiran

def ajukan_permohonan(permohonan_id):
    permohonan_spt_service = WorkFlowService(PermohonanSPT)
    spt_service = WorkFlowService(SPT)
    
    permohonan_spt_service.ajukan(permohonan_id)
    spt_service.ajukan(permohonan_id)
    
    return True

def simpan_permohonan(data, user, lampiran=None):
    """
    simpan permohonan (status = draft)

    Args:
        data (dict): data utama
        user (obj): instance user
        lampiran (spt_id: int, data: dict): data yang digunakan untuk upload lampiran
    """
    with transaction.atomic():
        # buat spt
        spt = SPT.objects.create(
            nomor_spt=data.get("nomor_spt"),
            judul=data.get("judul"),
            deskripsi=data.get("deskripsi"),
            tanggal_mulai=data.get("tanggal_mulai"),
            tanggal_selesai=data.get("tanggal_selesai"),
            dibuat_oleh=user,
            status="draft",
        )
        spt.save()
        
        # buat permohonan
        permohonan_spt = PermohonanSPT(
            spt=spt,
            tujuan=data.get("tujuan"),
            tanggal=data.get("tanggal"),
            dibuat_oleh=user,
            status="draft"
        )
        permohonan_spt.save()
        
        # buat lampiran
        if lampiran:
            for lamp in lampiran:
                data_lampiran = {
                    "file": lamp,
                    "keterangan": data.get("keterangan", ""),
                }
                upload_lampiran_spt(spt.id, data_lampiran)
                
        return permohonan_spt
