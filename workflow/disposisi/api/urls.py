from django.urls import path
from rest_framework.routers import DefaultRouter

from workflow.disposisi.api.viewsets import (
    DisposisiViewSet,
    
    # apiview
    DisposisiCreateView,
    DisposisiUpdateRevisiView
)

app_name = "disposisi_api"

router = DefaultRouter()
router.register(r"disposisi", DisposisiViewSet, basename="disposisi")

urlpatterns = [
    path("disposisi/create/", DisposisiCreateView.as_view(), name="disposisi_create"),
    path("kirim-revisi/<int:disposisi_id>/", DisposisiUpdateRevisiView.as_view(), name="kirim_revisi"),
]

urlpatterns += router.urls