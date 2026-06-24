from rest_framework.routers import DefaultRouter
from django.urls import path

from . import viewsets

app_name = "permohonan_api"

from spt.permohonan.api.viewsets import (
    PermohonanSPTViewSet,
    LampiranPermohonanSPTViewSet,
    
    # apiview
    PermohonanApiView
)

routers = DefaultRouter()
routers.register(r"permohonan-spt", viewset=PermohonanSPTViewSet, basename="permohonan-spt")
routers.register(r"lampiran-permohonan-spt", viewset=LampiranPermohonanSPTViewSet, basename="lampiran-permohonan-spt")

urlpatterns = [
    path("permohonan-list/", viewsets.PermohonanSPTListView.as_view(), name="permohohan-list"),
    path("create-permohonan/", PermohonanApiView.as_view(), name="create-permohonan"),
]

urlpatterns += routers.urls