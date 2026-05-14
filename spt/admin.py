from django.contrib import admin
from .models import SPT, SPTLampiran, NomorSuratSequence, PermohonanSPT, JenisSurat

admin.site.register(SPT)
admin.site.register(SPTLampiran)
admin.site.register(NomorSuratSequence)
admin.site.register(PermohonanSPT)
admin.site.register(JenisSurat)