from django.contrib import admin
from .models import SPT, SPTLampiran, NomorSuratSequence, PermohonanSPT, JenisSurat, LampiranPermohonanSPT

admin.site.register(SPT)
admin.site.register(SPTLampiran)
admin.site.register(NomorSuratSequence)
admin.site.register(PermohonanSPT)
admin.site.register(JenisSurat)
admin.site.register(LampiranPermohonanSPT)