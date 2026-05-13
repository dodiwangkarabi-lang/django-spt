from rest_framework import serializers
from tugas.models import TugasPelaksanaan, SuratPernyataanTugas
from spt.models import SPT
from django.contrib.auth.models import User

from spt.api.serializers import SPTSerializer

class SuratPernyataanTugasSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuratPernyataanTugas
        fields = '__all__'
        
class TugasPelaksanaanSerializer(serializers.ModelSerializer):
    surat_pernyataan_tugas = SuratPernyataanTugasSerializer(many=False, read_only=True)
    surat_pernyataan_tugas_id = serializers.PrimaryKeyRelatedField(
        queryset=SuratPernyataanTugas.objects.all(),
        source="surat_pernyataan_tugas",
        write_only=True
    )
    # spt = serializers.PrimaryKeyRelatedField(read_only=True)
    spt = SPTSerializer(many=False, read_only=True)
    spt_id = serializers.PrimaryKeyRelatedField(
        queryset=SPT.objects.all(),
        source="spt",
        write_only=True
    )
    
    pegawai = serializers.SerializerMethodField(read_only=True)
    pegawai_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="pegawai",
        write_only=True
    )
    
    def get_pegawai(self, obj):
        return {
            "id": obj.pegawai.id,
            "username": obj.pegawai.username,
            "email": obj.pegawai.email,
            "nama": obj.pegawai.profile.nama,
            "nip": obj.pegawai.profile.nip,
        }
    
    class Meta:
        model = TugasPelaksanaan
        fields = [
            "id",
            "spt",
            "spt_id",
            "pegawai",
            "pegawai_id",
            "keterangan",
            "hasil",
            "status",
            "lampiran",
            "surat_pernyataan_tugas",
            "surat_pernyataan_tugas_id",
        ]