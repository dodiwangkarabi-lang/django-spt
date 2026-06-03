from django.db import models
from django.conf import settings
from spt.models import SPT
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

class DisposisiTipe(models.TextChoices):
    INSTRUKSI = 'instruksi', 'instruksi'
    INFO = 'info', 'info'
    REQUEST = 'request', 'request'
    REVISI = 'revisi', 'revisi',
    SELESAI = 'selesai', 'selesai'
    
class DisposisiTemplate(models.Model):
    tipe = models.CharField(max_length=20, choices=DisposisiTipe.choices)
    teks_default = models.TextField()

    def __str__(self):
        return f"{self.get_tipe_display()} - {self.teks_default[:30]}"

class SPTApproval(models.Model):
    STATUS_CHOICES = (
        ('setuju', 'Setuju'),
        ('tolak', 'Tolak'),
        ('revisi', 'Revisi'),
    )

    spt = models.ForeignKey(
        SPT,
        on_delete=models.CASCADE,
        related_name='approvals'
    )
    approver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='approval_diberikan'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    catatan = models.TextField(blank=True)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.spt.nomor_spt} - {self.status}"

class Disposisi(models.Model):
    # STATUS_CHOICES = (
    #     ('diajukan', 'Diajukan'),
    #     ('disetujui', 'Disetujui'),
    #     ('ditolak', 'Ditolak'),
    # )

    spt = models.ForeignKey(
        SPT,
        on_delete=models.CASCADE,
        related_name='disposisi',
        blank=True, null=True
    )

    dari_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='disposisi_dikirim'
    )

    ke_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='disposisi_diterima'
    )

    status = models.CharField(max_length=20, choices=DisposisiTipe.choices)
    catatan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse('disposisi:disposisi_web:detail', kwargs={'disposisi_id': self.pk})
    
    @property
    def has_spt(self):
        return bool(self.spt)

    def __str__(self):
        return f"{self.pk} Disposisi"


class TandaTangan(models.Model):
    TIPE_CHOICES = (
        ('spt', 'SPT'),
        ('disposisi', 'Disposisi'),
    )

    spt = models.ForeignKey(
        SPT,
        on_delete=models.CASCADE,
        related_name='tanda_tangan'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tanda_tangan'
    )

    tipe = models.CharField(max_length=20, choices=TIPE_CHOICES)
    tanggal = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Tanda tangan {self.spt.nomor_spt}"