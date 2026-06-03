from rest_framework import serializers

# models
from spt.models import (
    SPT, SPTLampiran, SPTStatus
)

class SPTLampiranSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPTLampiran
        fields = '__all__'

class SPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPT
        fields = '__all__'
        
class SPTApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPT
        fields = ['status']
        

class SPTCatatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPT
        fields = ['catatan']

