from rest_framework import serializers
from .models import Dataset, Row

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ('id','name',)

class RowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Row
        fields = ('id','dataset_id','point','client_id', 'client_name')