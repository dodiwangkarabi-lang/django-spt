from django.urls import path

from . import views

app_name = "disposisi_web"

urlpatterns = [
    path("inbox/", views.inbox, name="inbox"),
    path("<int:disposisi_id>/", views.detail, name="detail"),
    path("inbox-detail/<int:disposisi_id>/", views.inbox_detail, name="inbox_detail"),
    # path("kirim-revisi/<int:disposisi_id>/", views.kirim_revisi, name="kirim_revisi"),
    path("", views.daftar_disposisi, name="list"),
]