from django.db.models import Q, F
from django.db.models.query import QuerySet

# models
from spt.models import (
    LampiranPermohonanSPT,
    PermohonanSPT
)

def get_lampiran_permohonan(permohonan_id: int) -> QuerySet:
    return LampiranPermohonanSPT.objects.filter(permohonan_spt=permohonan_id)

def get_permohonan() -> QuerySet:
    return PermohonanSPT.objects.all()

def get_permohonan_by_id(id: int):
    return PermohonanSPT.objects.get(id=id)
    