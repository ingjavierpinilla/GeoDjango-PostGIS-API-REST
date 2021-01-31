from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from rest_framework.settings import api_settings
from rest_framework.pagination import PageNumberPagination

from .serializer import DatasetSerializer, RowSerializer
from .models import Dataset, Row

class RowListView(APIView):


    def get(self, request, format=None):
        dataset_id = request.GET.get('dataset_id', None)
        name = request.GET.get('name', None)
        point = request.GET.get('point', None)

        if point is not None:
            point = point[1:-1].split(" ")
            if len(point) == 2:
                point = Point(float(point[0]), float(point[1]))
            else:
                return Response('Punto no valido.', status = status.HTTP_400_BAD_REQUEST)

        if dataset_id is None:
            return Response('Argumento dataset_id no encontrado.', status = status.HTTP_400_BAD_REQUEST)

        values = { 'dataset_id' : dataset_id, 'client_name' : name, 'point' : point}
        arguments = {}
        for k, v in values.items():
            if v:
                arguments[k] = v
                
        queryset = Row.objects.filter(**arguments)
        serializer = RowSerializer(queryset, many=True)
        return Response(serializer.data)
 


class Upload_csv(generics.ListCreateAPIView):

    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    pagination_class = PageNumberPagination


    def get_serializer_class(self):
        return DatasetSerializer


    def create(self, request, *args, **kwargs):
        try:

            if (name := request.data.get('name', None)) is None:
                return Response('nombre no encontrado.', status = status.HTTP_400_BAD_REQUEST)
            if (csv_file := request.FILES.get("file", None)) is None:
                return Response('csv no encontrado.', status = status.HTTP_400_BAD_REQUEST)

            if not csv_file.name.endswith('.csv'):
                return Response('Extension erronea.', status = status.HTTP_400_BAD_REQUEST)
            if csv_file.multiple_chunks():
                return Response(f'El archivo es muy grande ({(csv_file.size/(1000*1000))} MB).', status = status.HTTP_400_BAD_REQUEST)

            dataset_serializer = self.get_serializer(data = request.data, partial = True)
            if dataset_serializer.is_valid():
                dataset_serializer.save()

            pk = dataset_serializer.data.get('id')
            lines = csv_file.read().decode('utf-8').split('\n')
            for i, line in enumerate (lines):
                try:
                    if i != 0:
                        fields = line.split(",")
                        data_dict = {}
                        data_dict["dataset_id"] = pk
                        data_dict["point"] = Point(float(fields[0]), float(fields[1]))
                        data_dict["client_id"] = fields[2]
                        data_dict["client_name"] = fields[3]
                        row_serializer = RowSerializer(data = data_dict)
                        if row_serializer.is_valid():
                            row_serializer.save()
                except:
                    Dataset.objects.filter(id = pk).delete()
                    return Response(f'CSV corrupto en la linea {i}', status = status.HTTP_400_BAD_REQUEST)
            return Response(f'Carga exitosa', status = status.HTTP_200_OK)
        except Exception as e:
            return Response(f'Imposible cargar archivo {repr(e)}', status = status.HTTP_400_BAD_REQUEST)


