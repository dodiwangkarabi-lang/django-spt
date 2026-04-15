from django.urls import path
from . import views

urlpatterns = [
    # path("", views.spt, name="spt"),
    path("create/", views.spt_create, name="spt_create"),
    path("<int:spt_id>/update", views.spt_update, name="spt_update"),
    path("<int:spt_id>/", views.detail, name="spt_detail"),
    path("<int:spt_id>/remove/", views.remove, name="spt_remove"),
    path("<int:spt_id>/revisi/", views.revisi, name="spt_revisi"),
    path("<int:spt_id>/verifikasi/", views.verifikasi, name="spt_verifikasi"),
    path("<int:spt_id>/approve-final/", views.approve_final, name="spt_approve_final"),
    path("<int:spt_id>/ttd/", views.ttd, name="spt_ttd"),
    path("review/", views.review, name="spt_review"),
    path("<int:spt_id>/upload-lampiran/", views.upload_lampiran, name="spt_upload_lampiran"),
    path("delete-lampiran/<int:lampiran_id>/", views.delete_lampiran, name="spt_delete_lampiran"),
    path("<int:spt_id>/cetak/", views.cetak, name="spt_cetak"),
    path("<int:spt_id>/template-pdf/", views.template_pdf, name="template_pdf"),
    path("<int:spt_id>/preview/", views.preview, name="spt_preview"),
    path("spt/<int:spt_id>/action/", views.spt_action, name="spt_action"),
    path("", views.index, name="spt_index"),
]