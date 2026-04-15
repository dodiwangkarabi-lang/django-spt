from django.urls import path

from ..views.pegawai_views import *

urlpatterns = [
    path("grid-card", grid_card_htmx, name="pegawai_grid_card_htmx"),
    path("spt-list-diterima-htmx", spt_list_diterima_htmx, name="pegawai_spt_list_diterima_htmx"),
    path("spt-list-htmx", spt_list_htmx, name="pegawai_spt_list_htmx"),
]