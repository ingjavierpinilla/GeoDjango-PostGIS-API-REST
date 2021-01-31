from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from .serializer import DatasetSerializer, RowSerializer
from .models import Dataset
# Create your views here.
class Upload_csv(APIView):
    def post(self, request, *args, **kwargs):
        try:
            
            if((name := request.data.get("name")) and (csv_file := request.FILES["file"])):

                if not csv_file.name.endswith('.csv'):
                    return Response({'Extension erronea.'}, status = status.HTTP_400_BAD_REQUEST)
                if csv_file.multiple_chunks():
                    return Response({f'El archivo es muy grande ({(csv_file.size/(1000*1000))} MB).'}, status = status.HTTP_400_BAD_REQUEST)

                dataset_serializer = DatasetSerializer(data = request.data, partial = True)
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


