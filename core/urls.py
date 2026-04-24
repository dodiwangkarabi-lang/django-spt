from django.urls import path, include

from . import views

urlpatterns = [
    
    # permohonan
    path("permohonan/", views.permohonan_list, name="permohonan_list"),
    path("permohonan/<int:id>", views.permohonan_detail, name="permohonan_detail"),
    path("htmx/permohonan/", views.permohonan_list_htmx, name="permohonan_list_htmx"),
    
    # disposisi
    path("disposisi/", views.disposisi_list, name="disposisi_list"),
    path("disposisi/<int:disposisi_id>", views.disposisi_detail, name="disposisi_detail"),
    path("htmx/disposisi/", views.disposisi_list_htmx, name="disposisi_list_htmx"),
    
    # spt
    path("spt/", views.spt_list, name="spt_list"),
    path("spt/<int:spt_id>", views.spt_detail, name="spt_detail"),
    path("htmx/spt/", views.spt_list_htmx, name="spt_list_htmx"),
    # path("htmx/permohonan-spt/", views.permohonan_spt_list_htmx, name="permohonan_spt_list_htmx"),
    
    
    # pegawai
    path("pegawai/account-profile/", views.accounts_profile, name="accounts_profile"),
    path("pegawai/account-profile/edit", views.edit_profile, name="edit_profile"),
    path("pegawai/dashboard/", views.pegawai, name="core_pegawai_dashboard"),
    path("pegawai/spt-diterima/", views.spt_diterima, name="core_spt_diterima"),
    path("pegawai/spt-saya/", views.spt_saya, name="core_spt_saya"),
    path("pegawai/ajukan-spt/", views.ajukan_spt, name="core_ajukan_spt"),
    path("pegawai/ajukan-spt/<int:spt_id>/", views.kirim_pengajuan, name="core_kirim_pengajuan"),
    path("pegawai/spt-detail/<int:spt_id>/", views.spt_detail, name="core_spt_detail"),
    path("pegawai/<int:spt_id>/upload-laporan/", views.upload_laporan_oleh_pegawai, name="core_upload_laporan"),
    path("pegawai/<int:spt_id>/revisi/", views.spt_revisi, name="core_spt_revisi"),
    path("pegawai/<int:spt_id>/edit-revisi/", views.edit_revisi, name="core_edit_revisi"),
    path("pegawai/permohonan-spt/", views.permohonan_spt, name="core_permohonan_spt"), # tambahan
    path("pegawai/permohonan-spt/<int:id>", views.permohonan_spt_detail, name="core_permohonan_spt_detail"),
    path("pegawai/permohonan-spt/<int:id>/delete", views.permohonan_spt_delete, name="core_permohonan_spt_delete"),
    path("pegawai/htmx/", include('core.url_modules.pegawai_url_htmx')),
    
    
    # kasubag
    path("kasubag/dashboard/", views.kasubag, name="core_kasubag_dashboard"),
    path("kasubag/disposisi/", views.disposisi, name="core_kasubag_disposisi"),
    path("kasubag/<int:disposisi_id>/buat-spt/", views.buat_spt_kasubag_view, name="core_kasubag_buat_spt"),
    path("kasubag/daftar-spt-diajukan/", views.daftar_spt_diajukan, name="core_kasubag_daftar_spt_diajukan"),
    path("kasubag/<int:spt_id>/review-spt/", views.review_spt, name="core_kasubag_review_spt"),
    path("kasubag/review-permohonan/<int:disposisi_id>/", views.review_permohonan, name="core_kasubag_review_permohonan"),
    path("kasubag/disposisi/<int:disposisi_id>/", views.disposisi_detail, name="core_kasubag_disposisi_detail"),
    path("kasubag/approve/<int:disposisi_id>/", views.approve, name="core_kasubag_approve"),
    path("kasubag/reject/<int:disposisi_id>/", views.reject, name="core_kasubag_reject"),
    path("kasubag/revisi/<int:disposisi_id>/", views.revisi, name="core_kasubag_revisi"),
    path("kasubag/approval-spt/", views.approval_spt, name="core_kasubag_approval_spt"),
    path("kasubag/permohonan-spt/", views.kasubag_permohonan_spt, name="core_kasubag_permohonan_spt"), # tambahan
    path("kasubag/permohonan-spt/<int:id>", views.kasubag_permohonan_spt_detail, name="core_kasubag_permohonan_spt_detail"),
    path("kasubag/htmx/", include('core.url_modules.kasubag_url_htmx')),
    

    # pimpinan
    path("pimpinan/dashboard/", views.pimpinan, name="core_pimpinan_dashboard"),
    path("pimpinan/laporan-pelaksanaan/", views.laporan_pelaksanaan, name="core_pimpinan_laporan_pelaksanaan"),
    path("pimpinan/laporan-detail-pimpinan/<int:laporan_id>/", views.laporan_detail_pimpinan, name="core_pimpinan_laporan_detail_pimpinan"),
    path("pimpinan/disposisi/", views.disposisi_pimpinan, name="core_pimpinan_disposisi"),
    path("pimpinan/disposisi/<int:disposisi_id>/", views.disposisi_detail_pimpinan, name="core_pimpinan_disposisi_detail"),
    path("pimpinan/ttd/", views.ttd, name="core_pimpinan_ttd"),
    
    path("pimpinan/approval-final/", views.approval_final, name="core_pimpinan_approval_final"),
    path("pimpinan/setujui-permohonan/<int:disposisi_id>/", views.pimpinan_setujui_permohonan_view, name="core_pimpinan_setujui_permohonan"),
    path("pimpinan/approve/<int:disposisi_id>/", views.approve_pimpinan, name="core_pimpinan_approve"),
    path("pimpinan/reject/<int:disposisi_id>/", views.reject_pimpinan, name="core_pimpinan_reject"),
    path("pimpinan/revisi/<int:disposisi_id>/", views.revisi_pimpinan, name="core_pimpinan_revisi"),
    # path("pimpinan/detail-spt/", views.pimpoinan_detail_spt, name="core_pimpinan_detail_spt"),
    path("pimpinan/htmx/", include('core.url_modules.pimpinan_url_htmx')),
    
    
    # guests
    path("register/", views.register, name="core_register"),
    path("login/", views.login_view, name="core_login"),
    
    path("", views.index, name="core_index"),
]