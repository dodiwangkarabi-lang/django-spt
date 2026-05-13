from django.urls import path
from . import views

app_name = "spt_web"

urlpatterns = [
    path("permohonan/create/", views.permohonan_create, name="ajukan_permohonan"),
]