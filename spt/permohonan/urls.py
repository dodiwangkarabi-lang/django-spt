from django.urls import path, include

app_name = "permohonan"

urlpatterns = [
    path("htmx/", include("spt.permohonan.htmx.urls", namespace="permohonan_htmx")),
    path("api/", include("spt.permohonan.api.urls", namespace="permohonan_api")),
    path("", include("spt.permohonan.web.urls", namespace="permohonan_web")),
]