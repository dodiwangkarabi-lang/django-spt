from django.urls import path

from . import views

app_name = "permohonan_web"

urlpatterns = [
    path("create/", views.create, name="create"),
    path("<int:permohonan_id>/", views.detail, name="detail"),
    path("", views.index, name="list"),
    
]