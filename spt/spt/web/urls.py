from django.urls import path
from . import views

app_name = "spt_web"

urlpatterns = [
    path("<int:disposisi_id>/buat-spt/", views.create_spt, name="create_spt"),
    path("<int:spt_id>/review/", views.review_spt, name="review_spt"),
]