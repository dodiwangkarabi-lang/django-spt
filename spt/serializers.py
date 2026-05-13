from spt.models import SPT
from rest_framework import serializers

class SPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPT
        fields = '__all__'