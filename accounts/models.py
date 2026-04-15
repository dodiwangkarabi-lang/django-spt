from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100, blank=True, null=True)
    nip = models.CharField(max_length=50, blank=True)
    jabatan = models.CharField(max_length=100, blank=True)
    pangkat = models.CharField(max_length=100, blank=True)
    unit_kerja = models.CharField(max_length=100, blank=True)
    ttd = models.ImageField(upload_to='ttd/', blank=True, null=True)

    def __str__(self):
        return self.user.username