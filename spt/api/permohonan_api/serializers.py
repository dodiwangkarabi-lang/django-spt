from spt.models import PermohonanSPT
from rest_framework import serializers

class PermohonanSPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermohonanSPT
        fields = '__all__'