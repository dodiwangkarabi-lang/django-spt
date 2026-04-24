from django.urls import path

from ..views.kasubag_views import *

urlpatterns = [
    path("kasubag-permohonan-spt-list-htmx", kasubag_permohonan_spt_list_htmx, name="kasubag_permohonan_spt_list_htmx"),
]