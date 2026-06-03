from django.urls import path
from . import views

app_name = "permohonan_htmx"

urlpatterns = [
    path("", views.list_permohonan_view, name="list"),
]