from django.urls import path

from ..views.pimpinan_views import *

urlpatterns = [
    path("laporan-perjalanan-dinas-htmx", laporan_perjalanan_dinas_htmx, name="pimpinan_laporan_perjalanan_dinas_htmx"),
]