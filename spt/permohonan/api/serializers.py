from rest_framework import serializers

# models
from spt.models import (
    PermohonanSPT,
    LampiranPermohonanSPT
)

class LampiranPermohonanSPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = LampiranPermohonanSPT
        fields = '__all__'
        

class PermohonanSPTSerializer(serializers.ModelSerializer):
    lampiran = LampiranPermohonanSPTSerializer(many=True, read_only=True)
    class Meta:
        model = PermohonanSPT
        fields = '__all__'