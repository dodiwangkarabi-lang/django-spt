from django.db.models import Q, F
from django.shortcuts import get_object_or_404

# models
from spt.models import (
    SPT, SPTLampiran
)

def get_spt():
    return SPT.objects.all().order_by('-created_at')

def get_spt_by_user(user):
    return SPT.objects.filter(dibuat_oleh=user)

def get_spt_by_role(user):
    if user.groups.filter(name="pegawai").exists():
        return SPT.objects.filter(dibuat_oleh=user)

    if user.groups.filter(name="kasubag").exists():
        # return SPT.objects.filter(status="diajukan")
        qs = SPT.objects.all()
        return qs

    if user.groups.filter(name="pimpinan").exists():
        # return SPT.objects.filter(status="disetujui_kasubbag")
        qs = SPT.objects.all()
        return qs

    return SPT.objects.none()

def get_lampiran_by_spt(spt_id):
    spt = get_object_or_404(SPT, id=spt_id)
    return SPTLampiran.objects.filter(spt=spt)

def get_detail(spt_id):
    spt = get_object_or_404(SPT, id=spt_id)
    return spt