from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from rest_framework.settings import api_settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime, timezone

from .serializer import DatasetSerializer, RowSerializer, LogSerializer
from .models import Dataset, Row
from .utils import Mongologger
import re

logger = Mongologger()

def LogList(request):
    """FunctionView para presentar la tabla con los logs de consumo del API

    Args:
        request ([type]): [description]

    Returns:
        [render]: [html usando bootstrap para presentar la tabla de logs]
    """
    permission_classes = (AllowAny,)
    return render(request, "log/log_table.html")

class LogListView(generics.ListAPIView):
    """ListView de los logs, requiere de token JWT

    Args:
        generics ([type]): [description]

    Returns:
        JSON con lso registros de consumo del API
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = LogSerializer
    pagination_class = None
    def get_queryset(self):
        return logger.get_querryset()

class RowListView(APIView):
    """ListView de las filas de un determinado dataset,, recibe los query parameters dataset_id (obligatorio), name y point (opcionales)
        cuenta unicamente con metodo GET
    Args:
        APIView ([type]): [description]

    Returns:
        [type]: [description]
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            dataset_id = int(request.GET.get('dataset_id', None))
        except:
            return Response('dataset_id debe existir y ser un entero.', status = status.HTTP_400_BAD_REQUEST)

        name = request.GET.get('name', None)
        point = request.GET.get('point', None)

        if point is not None:
            try:
                point = point.replace('(', ' ').replace(')', '').replace(' ', '').split(",")
                if len(point) == 2:
                    point = Point(float(point[0]), float(point[1]))
                else:
                    return Response('Punto no valido.', status = status.HTTP_400_BAD_REQUEST)
            except:
                return Response('Punto no valido.', status = status.HTTP_400_BAD_REQUEST)

        values = { 'dataset_id' : dataset_id, 'client_name' : name, 'point' : point}
        arguments = {}

        for k, v in values.items():
            if v:
                arguments[k] = v
                
        queryset = Row.objects.filter(**arguments)
        serializer = RowSerializer(queryset, many=True)
        logger.log(request)

        return Response(serializer.data)
 


class DatasetListCreate(generics.ListCreateAPIView):
    """ListCreateAPIView para los datasets, cuenta con metodo GET y POST, para el metodo POST son obligatorios los parametros name y file 

    Args:
        generics ([type]): [description]

    Returns:
        [type]: [description]
    """
    permission_classes = (IsAuthenticated,) 
    serializer_class = DatasetSerializer
    pagination_class = PageNumberPagination
    

    def get_serializer_class(self):
        return DatasetSerializer

    def get_queryset(self):
        """Obtiene todos los datasets almacenados en la base de datos
        """
        #log del consumo del metodo GET de la clase
        logger.log(self.request)
        return Dataset.objects.all().order_by('-id')

    def create(self, request, *args, **kwargs):
        """Se agrega un nuevo dataset a la base de datos, por cada peticion de tipo POST se verifica
        que se envie un nombre no vacio y un archivo con extension *.csv. Del archivo se ignora la columna
        de encabezado y se esperan 4 columnas.

        Args:
            request ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:

            if len((name := request.data.get('name', ''))) == 0:
                return Response('nombre no encontrado.', status = status.HTTP_400_BAD_REQUEST)
            if (csv_file := request.FILES.get("file", None)) is None:
                return Response('csv no encontrado.', status = status.HTTP_400_BAD_REQUEST)

            if not csv_file.name.endswith('.csv'):
                return Response('Extension erronea.', status = status.HTTP_400_BAD_REQUEST)
            if csv_file.multiple_chunks():
                return Response(f'El archivo es muy grande ({(csv_file.size/(1000*1000))} MB).', status = status.HTTP_400_BAD_REQUEST)
            
            #Creacion de dataset previo a la creacion de las filas
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
                    #Si alguna de las filas contiene un error se elimina el dataset completamente
                    Dataset.objects.filter(id = pk).delete()
                    return Response(f'CSV corrupto en la linea {i}', status = status.HTTP_400_BAD_REQUEST)
            logger.log(request)
            return Response(f'Carga exitosa', status = status.HTTP_200_OK)
        except Exception as e:
            return Response(f'Imposible cargar archivo {repr(e)}', status = status.HTTP_400_BAD_REQUEST)


