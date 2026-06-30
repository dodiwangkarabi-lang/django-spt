from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

# models.py
from django.db import models

# selectors
from accounts.selectors.selectors import (
    get_kasubag_user, get_pegawai_user, get_pimpinan_user
)

class SuratPernyataan(models.Model):
    spt = models.OneToOneField(
        'spt.SPT',
        on_delete=models.CASCADE,
        related_name='surat_pernyataan',
        blank=True,
        null=True
    )
    isi = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.pk} Surat Pernyataan"

class JenisSurat(models.Model):
    nama = models.CharField(max_length=100)
    kode = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.kode} - {self.nama}"

class NomorSuratSequence(models.Model):
    jenis_surat = models.ForeignKey(
        JenisSurat, on_delete=models.CASCADE, related_name='sequences',
        null=True,
        blank=True
    )
    tahun = models.IntegerField()
    bulan = models.IntegerField()
    nomor_akhir = models.IntegerField(default=0)

    class Meta:
        unique_together = ('jenis_surat', 'tahun', 'bulan')

    def __str__(self):
        return f"{self.pk} {self.tahun}-{self.bulan}: {self.nomor_akhir}"

class SPTStatus(models.TextChoices):
    DRAFT = "draft", "draft"
    PERMOHONAN_DIAJUKAN = "permohonan_diajukan", "Permohonan Diajukan"
    
    KASUBAG_REVIEW = "KASUBAG_REVIEW", "Kasubag Review"
    KASUBAG_SETUJUI = "KASUBAG_SETUJUI", "Kasubag Setujui"
    KASUBAG_SETUJUI_PERMOHOAN = "KASUBAG_SETUJUI_PERMOHOAN", "Kasubag Setujui Permohonan"
    KASUBAG_AJUKAN_SPT = "kasubag_ajukan_spt", "Kasubag Ajukan SPT"

    KEPALA_REVIEW_PERMOHONAN = "KEPALA_REVIEW_PERMOHONAN", "Kepala Review Permohonan"
    KEPALA_SETUJUI_PERMOHONAN = "KEPALA_SETUJUI_PERMOHONAN", "Kepala Setujui Permohonan"

    SPT_DIBUAT = "SPT_DIBUAT", "SPT Dibuat"

    KEPALA_REVIEW_SPT = "KEPALA_REVIEW_SPT", "Kepala Review SPT"
    KEPALA_SETUJUI_SPT = "KEPALA_SETUJUI_SPT", "Kepala Setujui SPT"

    TTD_SPT = "TTD_SPT", "Tanda Tangan SPT"

    DITOLAK = "ditolak", "Ditolak"
    
    DIAJUKAN = "diajukan", "diajukan"
    DISETUJUI = "disetujui", "disetujui"
    FINAL = "final", "final"
    SELESAI = "selesai", "selesai"
    REVISI = "direvisi", "Direvisi"
    
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
    
    @property
    def has_surat_pernyataan(self):
        # has attribute
        return hasattr(self, "surat_pernyataan")
    
    def get_absolute_url(self):
        return reverse('spt:spt_web:review_spt', kwargs={'spt_id': self.pk})
    
    @property
    def can_edit(self)->bool:
        # kasubag user
        kasubag = get_kasubag_user()
        status = self.status == SPTStatus.REVISI
        return kasubag and status
    
    @property
    def is_disetujui(self):
        return self.status == SPTStatus.DISETUJUI
    
    @property
    def is_direvisi(self):
        return self.status == SPTStatus.DIREVISI
    
    @property
    def is_ditolak_pimpinan(self):
        return self.status == SPTStatus.DITOLAK_PIMPINAN
    
    @property
    def is_ditolak(self):
        return self.status == SPTStatus.DITOLAK
    
    @property
    def is_diajukan(self):
        return self.status == SPTStatus.DIAJUKAN
    
    @property
    def is_draft(self):
        return self.status == SPTStatus.DRAFT
    
    @property
    def is_review_kasubag(self):
        return self.status == SPTStatus.REVIEW_KASUBAG
    
    def has_status(self, *statuses):
        return self.status in statuses

    def __str__(self):
        return f"{self.pk} {self.nomor_spt}"
    
class PermohonanSPT(models.Model):
    
    spt = models.OneToOneField(
       SPT,
       on_delete=models.CASCADE,
       related_name='permohonan_spt',
       blank=True,
       null=True 
    )
    judul = models.CharField(max_length=255, blank=True, null=True)
    deskripsi = models.TextField(blank=True, null=True)
    catatan = models.TextField(blank=True, null=True, default="")
    tanggal_mulai = models.DateField(blank=True, null=True)
    tanggal_selesai = models.DateField(blank=True, null=True)
    dibuat_oleh = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='permohonan_spt',
        blank=True,
        null=True
    )
    status = models.CharField(max_length=100, choices=SPTStatus.choices, default=SPTStatus.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse('permohonan:permohonan_web:detail', kwargs={'permohonan_id': self.pk})
    
    class Meta:
        ordering=['-created_at']
    
    def __str__(self):
        return f"{self.pk} Permohonan SPT"
    
class LampiranPermohonanSPT(models.Model):
    permohonan_spt = models.ForeignKey(
        PermohonanSPT,
        on_delete=models.CASCADE,
        related_name='lampiran'
    )
    file = models.FileField(upload_to='lampiran_permohonan_spt/')
    keterangan = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.pk} Lampiran {self.permohonan_spt.id}"
    
class SPTLampiran(models.Model):
    spt = models.ForeignKey(
        SPT,
        on_delete=models.CASCADE,
        related_name='lampiran'
    )
    file = models.FileField(upload_to='lampiran_spt/')
    keterangan = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"Lampiran {self.spt.nomor_spt}"