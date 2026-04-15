from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import TugasPelaksanaan
from spt.models import SPT
from django.http import QueryDict

from django.shortcuts import get_object_or_404

@transaction.atomic
def upload_laporan_service(request, spt_id, data: dict = None):
    data = data or {}

    spt = get_object_or_404(SPT, id=spt_id)
    # update spt
    spt.status = "selesai"
    spt.save()

    defaults = {
        "pegawai": request.user,
        "laporan": data.get("laporan", ""),
        "status": data.get("status", "proses"),
        "keterangan": data.get("keterangan"),
        "hasil": data.get("hasil"),
        "lampiran": data.get("lampiran"),
    }
    
    
    obj = TugasPelaksanaan.objects.filter(spt=spt).first()

    if obj:
        # UPDATE
        if obj:
            for key, value in defaults.items():
                setattr(obj, key, value)
            obj.save()
            return obj

    
    
    # CREATE
    return TugasPelaksanaan.objects.create(
        spt=spt,
        **defaults
    )

def is_laporan_exist(spt_id):
    """
    Mengecek apakah spt yang sudah di laksananan sudah ada laporannya atau belum

    Args:
        spt_id (str): id spt

    Returns:
        Bool : Benar atau Salah
    """
    obj = TugasPelaksanaan.objects.filter(spt_id=spt_id).first()
    return obj