from .views import SPTDetailApi, SPTListCreateApi
from django.urls import path

app_name = "spt_api" 

urlpatterns = [
    path("", SPTListCreateApi.as_view(), name="spt-list-create"),
    path("<int:spt_id>/", SPTDetailApi.as_view(), name="spt-detail"),
]

