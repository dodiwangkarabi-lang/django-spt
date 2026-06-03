from django.urls import path

from spt.spt.api.viewsets import (
    TolakSPTAPIView, RevisiSPTAPIView, TerimaSPTAPIView,
    SimpanBanyakLampiranView, HapusLampiranView,
    ListLampiranView, KirimRevisiSPT
)

app_name = "spt_api"

urlpatterns = [
    path("kirim-revisi-spt/<int:spt_id>/", KirimRevisiSPT.as_view(), name="kirim_revisi_spt"),
    path("list-lampiran/<int:spt_id>/", ListLampiranView.as_view(), name="list_lampiran"),
    path("hapus-lampiran/<int:lampiran_id>/", HapusLampiranView.as_view(), name="hapus_lampiran"),
    path("simpan-banyak-lampiran/<int:spt_id>/", SimpanBanyakLampiranView.as_view(), name="simpan_banyak_lampiran"),
    path("tolak-sptku/<int:spt_id>/", TolakSPTAPIView.as_view(), name="tolak_sptku"),
    path("revisi-sptku/<int:spt_id>/", RevisiSPTAPIView.as_view(), name="revisi_sptku"),
    path("terima-sptku/<int:spt_id>/", TerimaSPTAPIView.as_view(), name="terima_sptku"),
]