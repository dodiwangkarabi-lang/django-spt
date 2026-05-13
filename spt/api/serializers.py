# models
from spt.models import SPT, PermohonanSPT
from workflow.models import Disposisi

from rest_framework import serializers


class SPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPT
        fields = '__all__'
        
class PermohonanSPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermohonanSPT
        fields = '__all__'
        
class SetujuiPermohonanSPTSerializer(serializers.ModelSerializer):
    disposisi_id = serializers.IntegerField()
    
    class Meta:
        model = Disposisi
        fields = ["disposisi_id"]