from .views import TugasPelaksanaanView
from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns

app_name = "tugas_api"

urlpatterns = [
    path("<int:tugas_pelaksanaan_id>/tugas-pelaksanaan/", TugasPelaksanaanView.as_view(), name="tugas-pelaksanaan"),
]