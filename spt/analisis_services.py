from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone

from .models import SPT, SPTLampiran, SPTStatus
from tugas.models import TugasPelaksanaan
from workflow.models import Disposisi, DisposisiTemplate, DisposisiTipe

class RangkumanSPT:
    def __init__(self):
        self.spt = SPT.objects.all()
    
    
    def total_spt(self):
        return self.spt.count()
    
   
    def total_spt_disetujui(self):
        filtered = self.spt.filter(status=SPTStatus.DISETUJUI_FINAL)
        return filtered.count()
    
    def total_laporan_selesai(self):
        filtered = TugasPelaksanaan.objects.all()
        return filtered.count()
    
    def total_proses_review_kasubag(self):
        filtered = self.spt.filter(status=SPTStatus.REVIEW_KASUBAG)
        return filtered.count()
    
    def total_permohonan_belum_direview(self):
        filtered = self.spt.filter(status=SPTStatus.PERMOHONAN_DIAJUKAN)
        return filtered.count()