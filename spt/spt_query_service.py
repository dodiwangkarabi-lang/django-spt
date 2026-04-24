from spt.models import SPT
from django.db.models import Q, QuerySet

def get_all_spt() -> QuerySet[SPT]:
    return SPT.objects.all()

def get_spt_by_id(spt_id) -> SPT:
    return SPT.objects.get(id=spt_id)

def get_spt_by_nomor_spt(nomor_spt) -> QuerySet[SPT]:
    return SPT.objects.filter(nomor_spt=nomor_spt)



