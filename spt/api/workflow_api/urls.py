from django.urls import path
from .ajukan_spt import AjukanSPTAPIView

app_name = 'workflow_api'

urlpatterns = [
    path("ajukan/<int:spt_id>/", AjukanSPTAPIView.as_view(), name="ajukan_spt"),
]