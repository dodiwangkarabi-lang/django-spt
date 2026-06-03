from django.urls import path, include

app_name = "disposisi"

urlpatterns = [
    path("api/", include("workflow.disposisi.api.urls", namespace="disposisi_api")),
    path("", include("workflow.disposisi.web.urls", namespace="disposisi_web")),
]