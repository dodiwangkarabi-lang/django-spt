from django.db import models
from django.contrib.auth.models import User

# models.py
from django.db import models

class NomorSuratSequence(models.Model):
    tahun = models.IntegerField()
    bulan = models.IntegerField()
    nomor_akhir = models.IntegerField(default=0)

    class Meta:
        unique_together = ('tahun', 'bulan')

    def __str__(self):
        return f"{self.tahun}-{self.bulan}: {self.nomor_akhir}"

class SPTStatus(models.TextChoices):
    DRAFT = "draft", "draft"
    PERMOHONAN_DIAJUKAN = "permohonan_diajukan", "Permohonan Diajukan"
    
    KASUBAG_REVIEW = "KASUBAG_REVIEW", "Kasubag Review"
    KASUBAG_SETUJUI = "KASUBAG_SETUJUI", "Kasubag Setujui"
    KASUBAG_AJUKAN_SPT = "kasubag_ajukan_spt", "Kasubag Ajukan SPT"

    KEPALA_REVIEW_PERMOHONAN = "KEPALA_REVIEW_PERMOHONAN", "Kepala Review Permohonan"
    KEPALA_SETUJUI_PERMOHONAN = "KEPALA_SETUJUI_PERMOHONAN", "Kepala Setujui Permohonan"

    SPT_DIBUAT = "SPT_DIBUAT", "SPT Dibuat"

    KEPALA_REVIEW_SPT = "KEPALA_REVIEW_SPT", "Kepala Review SPT"
    KEPALA_SETUJUI_SPT = "KEPALA_SETUJUI_SPT", "Kepala Setujui SPT"

    TTD_SPT = "TTD_SPT", "Tanda Tangan SPT"

    DITOLAK = "DITOLAK", "Ditolak"
    
    DIAJUKAN = "diajukan", "diajukan"
    DISETUJUI = "disetujui", "disetujui"
    FINAL = "final", "final"
    SELESAI = "selesai", "selesai"
    REVISI = "revisi", "revisi"
    
    REVIEW_KASUBAG = "review_kasubbag", "review_kasubbag"
    REVISI_KASUBAG = "revisi_kasubbag", "revisi_kasubbag"
    DISETUJUI_FINAL = "disetujui_final", "disetujui_final"
    DITOLAK_PIMPINAN = "ditolak_pimpinan", "ditolak_pimpinan"
    REVISI_PIMPINAN = "revisi_pimpinan", "revisi_pimpinan"
    
    REVIEW_PIMPINAN = "review_pimpinan", "review_pimpinan"
    DITOLAK_KASUBAG = "ditolak_kasubbag", "ditolak_kasubbag",
    DIAJUKAN_ULANG = "diajukan_ulang", "diajukan_ulang"
    PELAKSANAAN = "pelaksanaan", "pelaksanaan"
    
    
    
    # pimpinan
    PERMOHONAN_DISETUJUI_PIMPINAN = "permohonan_disetujui_pimpinan", "permohonan_disetujui_pimpinan"
    REVIEW_SPT_PIMPINAN = "review_spt_pimpinan", "review_spt_pimpinan"

class SPT(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('diajukan', 'Diajukan'),
        ('disetujui', 'Disetujui'),
        ('ditolak', 'Ditolak'),
        ('direvisi', 'Direvisi'),
    )
    nomor_spt = models.CharField(max_length=100)
    judul = models.CharField(max_length=255)
    deskripsi = models.TextField(blank=True)
    catatan = models.TextField(blank=True, null=True, default="")
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    dibuat_oleh = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='spt_dibuat'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nomor_spt
    
class SPTLampiran(models.Model):
    spt = models.ForeignKey(
        SPT,
        on_delete=models.CASCADE,
        related_name='lampiran'
    )
    file = models.FileField(upload_to='lampiran_spt/')
    keterangan = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Lampiran {self.spt.nomor_spt}"