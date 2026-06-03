from django.urls import path, include

app_name = "spt"

urlpatterns = [
    path("api/", include("spt.spt.api.urls", namespace="spt_api")),
    path("web/", include("spt.spt.web.urls", namespace="spt_web")),
    # path("htmx/", include("spt.htmx.urls", namespace="spt_htmx")),
]