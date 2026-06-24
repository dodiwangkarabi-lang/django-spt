from django.urls import path, include
from rest_framework.routers import DefaultRouter
from spt.api.viewsets import PermohonanSPTViewSet, SPTViewSet

from . import views

app_name = 'spt_api'

# default router
# router = DefaultRouter()    

# router.register(r'permohonan-sptq', PermohonanSPTViewSet, basename='permohonan-sptq')
# router.register(r'sptq', SPTViewSet, basename='sptq')

urlpatterns = [
    # path("workflow/", include("spt.api.workflow_api.urls", namespace="workflow_api")),
    # path('spt/', include("spt.api.spt_api.urls", namespace="spt_api")),
    
    path(
        "permohonan-sptq/",
        PermohonanSPTViewSet.as_view({
            "get": "list",
            "post": "create",
        })
    ),
    
    
    path('spt/<int:spt_id>/cetak/pdf/', views.CetakLaporanPelaksaanTugas.as_view(), name='cetak_pdf'),
]

# urlpatterns += router.urls












# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()

# print("router dibuat")

# urlpatterns = []

# print("sebelum urls")

# x = router.urls

# print("sesudah urls")

# urlpatterns += x