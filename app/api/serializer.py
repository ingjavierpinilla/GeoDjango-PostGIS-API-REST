from rest_framework import serializers
from .models import Dataset, Row
from django.forms.fields import GenericIPAddressField

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        ordering = ['-id']
        fields = ('id','name', 'date')

class RowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Row
        ordering = ['-id']
        fields = ('id','dataset_id','point','client_id', 'client_name')
