from rest_framework import serializers

# models
from workflow.models import Disposisi

class DisposisiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disposisi
        fields = '__all__'