from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView

# Create your views here.
class Upload_csv(APIView):
    def post(self, request):
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            return Response({'Extension erronea.'}, status = status.HTTP_400_BAD_REQUEST)
        if csv_file.multiple_chunks():
            return Response({f'El archivo es muy grande ({(csv_file.size/(1000*1000))} MB).'}, status = status.HTTP_400_BAD_REQUEST)