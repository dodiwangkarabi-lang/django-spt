from django.db import models
from django.conf import settings
from spt.models import SPT
from django.contrib.auth.models import User


class TugasPelaksanaan(models.Model):
    STATUS_CHOICES = (
        ('belum', 'Belum'),
        ('proses', 'Proses'),
        ('selesai', 'Selesai'),
    )


    spt = models.ForeignKey(
        SPT,
        on_delete=models.CASCADE,
        related_name='tugas'
    )


    pegawai = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tugas_dikerjakan'
    )


    laporan = models.TextField(blank=True)
    keterangan = models.TextField(blank=True, null=True, default="")
    hasil = models.TextField(blank=True, null=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='belum')
    lampiran = models.FileField(upload_to='lampiran_tugas/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


    def __str__(self):
        return f"{self.pk} Tugas {self.spt.nomor_spt}"
    
class SuratPernyataanTugas(models.Model):
    tugas_pelaksanaan = models.OneToOneField('tugas.TugasPelaksanaan', on_delete=models.CASCADE, null=True, blank=True, related_name='surat_pernyataan_tugas')
    
    surat_pernyataan = models.TextField(blank=True, null=True, default="")
    tanggal = models.DateField(null=True, blank=True)
    no_surat = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.pk} surat pernyataan"