from django.contrib import admin
from .models import TandaTangan, Disposisi, SPTApproval, DisposisiTemplate

admin.site.register(DisposisiTemplate)

@admin.register(TandaTangan)
class TandaTanganAdmin(admin.ModelAdmin):
    pass

@admin.register(Disposisi)
class DisposisiAdmin(admin.ModelAdmin):
    pass

@admin.register(SPTApproval)
class SPTApprovalAdmin(admin.ModelAdmin):
    pass
