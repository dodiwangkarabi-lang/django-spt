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
    
    # --------------------SPTViewset--------------------
    path(
        "sptq/",
        SPTViewSet.as_view({
            "get": "list",
            "post": "create",
        })
    ),
    
    path(
        "sptq/<int:pk>/",
        SPTViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        })
    ),
    
    # Action custom
    path(
        "sptq/<int:pk>/tolak-spt/",
        SPTViewSet.as_view({
            "post": "tolak_spt",
        }),
        name="spt-tolak"
    ),

    path(
        "sptq/<int:pk>/revisi-spt/",
        SPTViewSet.as_view({
            "post": "revisi_spt",
        }),
        name="spt-revisi"
    ),

    path(
        "sptq/<int:pk>/setujui-spt/",
        SPTViewSet.as_view({
            "post": "setujui_spt",
        }),
        name="spt-setujui"
    ),
    
    # --------------------Permohonan--------------------
    
    
    path(
        "permohonan-sptq/",
        PermohonanSPTViewSet.as_view({
            "get": "list",
            "post": "create",
        })
    ),
    
    path(
        "permohonan-sptq/<int:pk>/",
        PermohonanSPTViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        })
    ),
    
    # action
    path(
        "permohonan-sptq/<int:pk>/ajukan-permohonan/",
        PermohonanSPTViewSet.as_view({
            "post": "ajukan_permohonan",
        }),
        name="permohonan-spt-ajukan"
    ),

    path(
        "permohonan-sptq/<int:pk>/tolak-permohonan/",
        PermohonanSPTViewSet.as_view({
            "post": "tolak_permohonan",
        }),
        name="permohonan-spt-tolak"
    ),

    path(
        "permohonan-sptq/<int:pk>/revisi-permohonan/",
        PermohonanSPTViewSet.as_view({
            "post": "revisi_permohonan",
        }),
        name="permohonan-spt-revisi"
    ),

    path(
        "permohonan-sptq/<int:pk>/setujui-permohonan/",
        PermohonanSPTViewSet.as_view({
            "post": "setujui_permohonan",
        }),
        name="permohonan-spt-setujui"
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