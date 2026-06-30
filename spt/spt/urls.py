from django.urls import path, include

from spt.web import views

app_name = "spt"

urlpatterns = [
    path("surat-pernyataan/<int:surat_pernyataan_id>/cetak/", views.cetak_surat_pernyataan, name="cetak_surat_pernyataan"),
    path("<int:spt_id>/surat-pernyataan/", views.surat_pernyataan, name="surat_pernyataan"),
    path("api/", include("spt.spt.api.urls", namespace="spt_api")),
    path("web/", include("spt.spt.web.urls", namespace="spt_web")),
    # path("htmx/", include("spt.htmx.urls", namespace="spt_htmx")),
]