from django.urls import path
from .views import Upload_csv

urlpatterns = [
    path('v1/datasets', Upload_csv.as_view()),

]
