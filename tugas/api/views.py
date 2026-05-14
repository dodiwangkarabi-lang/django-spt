from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

# services
from core.services import generate_nomor_surat

# models
from tugas.models import TugasPelaksanaan, SuratPernyataanTugas
from spt.models import JenisSurat

# serializers
from tugas.api.serializers import TugasPelaksanaanSerializer, SuratPernyataanTugasSerializer

class TugasPelaksanaanView(APIView):
    def get(self, request, tugas_pelaksanaan_id, format=None):
        tugas_pelaksanaan = (
            TugasPelaksanaan.objects
            .select_related("surat_pernyataan_tugas", "spt", "pegawai")
            .get(id=tugas_pelaksanaan_id)
        )
        
        return Response({
            "message": "data ditemukan",
            "data": TugasPelaksanaanSerializer(tugas_pelaksanaan, many=False).data,
            "success": True
        }, status=status.HTTP_200_OK)
    
    def post(self, request, tugas_pelaksanaan_id, format=None):
        formData = request.data.copy()
        
        tugas_pelaksanaan = TugasPelaksanaan.objects.get(id=tugas_pelaksanaan_id)
        tanggal = datetime.strptime(formData.get("tanggal"), "%Y-%m-%d")
        no_surat = generate_nomor_surat(jenis_surat=JenisSurat.objects.get(kode="SPMT"), tanggal=tanggal)
        
        obj, created = SuratPernyataanTugas.objects.update_or_create(
            tugas_pelaksanaan=tugas_pelaksanaan,
            defaults={
                "tanggal": tanggal,
                "no_surat": no_surat,
            }
        )
        
        return Response({
            "message": f"berhasil {'update' if not created else 'create'} data",
            "success": True,
            # "data": SuratPernyataanTugasSerializer(SuratPernyataanTugas.objects.get(tugas_pelaksanaan=tugas_pelaksanaan), many=False).data
        }, status=status.HTTP_201_CREATED)
        
        
    def delete(self, request, tugas_pelaksanaan_id, format=None):
        tugas_pelaksanaan = TugasPelaksanaan.objects.get(id=tugas_pelaksanaan_id)
        surat_pernyataan_tugas = SuratPernyataanTugas.objects.get(tugas_pelaksanaan=tugas_pelaksanaan)
        surat_pernyataan_tugas.delete()
        
        return Response({
            "message": "berhasil menghapus data",
            "success": True,
            "data": None
        }, status=status.HTTP_204_NO_CONTENT)