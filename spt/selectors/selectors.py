from django.db.models import Q, QuerySet

from core.permissions.roles import (
    ROLE_KASUBAG, ROLE_PEGAWAI, ROLE_PIMPINAN
)

# models
from spt.models import (
    SPTStatus, SPT
)

def get_spt_diterima_all() -> QuerySet[SPT]:
    qs = SPT.objects.filter(status=SPTStatus.DISETUJUI)
    return qs

def get_spt_all() -> QuerySet[SPT]:
    qs = SPT.objects.all()
    return qs

def get_spt_diterima_list_by_user(user) -> QuerySet[SPT]:
    if user.groups.filter(name=ROLE_PEGAWAI).exists():
        qs = (
            SPT.objects.filter(dibuat_oleh=user)
            .filter(
                Q(status=SPTStatus.DISETUJUI)
        #         Q(status="disetujui_final") |
        #         Q(status="selesai") |
        #         Q(status=SPTStatus.DISETUJUI)
            )
        )
        # qs = SPT.objects.all()
        return qs

    if user.groups.filter(name=ROLE_PIMPINAN).exists():
        return SPT.objects.filter(status=SPTStatus.DIAJUKAN)

    return SPT.objects.none()